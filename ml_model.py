import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from threading import Lock, Thread

from ml_model_compat import (
    format_prediction,
    load_or_build_model,
    load_class_names,
    preprocess_image_bytes,
)


BASE_DIR = Path(__file__).resolve().parent
COMPAT_RUNNER_PATH = BASE_DIR / "ml_compat_runner.py"
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
FALLBACK_TIMEOUT_SECONDS = int(os.environ.get("PIGILAN_ML_FALLBACK_TIMEOUT_SECONDS", "600"))

_warmup_lock = Lock()
_warmup_thread = None
_warmup_error = None
_model_lock = Lock()
_model = None


def get_model():
    global _model

    if _model is not None:
        return _model

    with _model_lock:
        if _model is None:
            import tensorflow as tf

            _model = load_or_build_model(tf)

    return _model


def get_class_names():
    return load_class_names()


def _is_model_ready():
    return _model is not None


def _warm_model_in_background():
    global _warmup_error

    try:
        get_model()
        _warmup_error = None
    except Exception as exc:
        _warmup_error = exc


def start_model_warmup():
    global _warmup_thread

    if _is_model_ready():
        return get_model_warmup_state()

    with _warmup_lock:
        if _warmup_thread is None or not _warmup_thread.is_alive():
            _warmup_thread = Thread(
                target=_warm_model_in_background,
                name="pigilan-ml-warmup",
                daemon=True,
            )
            _warmup_thread.start()

    return get_model_warmup_state()


def get_model_warmup_state():
    if _is_model_ready():
        return {
            "status": "ready",
            "message": "Photo AI is ready.",
        }

    if _warmup_thread is not None and _warmup_thread.is_alive():
        return {
            "status": "loading",
            "message": (
                "Preparing photo AI in the background. The first check after opening "
                "the app may still take a while, but later checks should be much faster."
            ),
        }

    if _warmup_error is not None:
        return {
            "status": "error",
            "message": f"Photo AI warm-up failed: {_warmup_error}",
        }

    return {
        "status": "idle",
        "message": "Photo AI has not started loading yet.",
    }


def _read_uploaded_file_bytes(uploaded_file):
    if hasattr(uploaded_file, "getvalue"):
        image_bytes = uploaded_file.getvalue()
    else:
        uploaded_file.seek(0)
        image_bytes = uploaded_file.read()

    safe_name = Path(getattr(uploaded_file, "name", "uploaded_image.jpg")).name
    suffix = Path(safe_name).suffix or ".jpg"
    return image_bytes, suffix


def _candidate_python_executables():
    seen = set()
    candidates = []

    if sys.platform.startswith("win"):
        base_python = Path(sys.base_prefix) / "python.exe"
    else:
        base_python = Path(sys.base_prefix) / "bin" / "python"
    candidates.append(base_python)
    candidates.append(Path(sys.executable))

    python_on_path = shutil.which("python")
    if python_on_path:
        candidates.append(Path(python_on_path))

    for candidate in candidates:
        try:
            resolved = str(candidate.resolve())
        except Exception:
            resolved = str(candidate)
        if resolved in seen or not candidate.exists():
            continue
        seen.add(resolved)
        yield candidate


def _predict_with_current_runtime(image_bytes):
    model = get_model()
    prediction = model.predict(preprocess_image_bytes(image_bytes), verbose=0)
    return format_prediction(prediction, get_class_names())


def _predict_with_fallback_runtime(image_bytes, suffix):
    runner_errors = []
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(image_bytes)
            temp_path = Path(temp_file.name)

        for python_executable in _candidate_python_executables():
            try:
                completed = subprocess.run(
                    [str(python_executable), str(COMPAT_RUNNER_PATH), str(temp_path)],
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    text=True,
                    timeout=FALLBACK_TIMEOUT_SECONDS,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                runner_errors.append(
                    f"{python_executable}: Timed out after {FALLBACK_TIMEOUT_SECONDS} seconds."
                )
                continue
            except OSError as exc:
                runner_errors.append(f"{python_executable}: {exc}")
                continue

            if completed.returncode == 0:
                return json.loads(completed.stdout.strip())

            error_output = completed.stderr.strip() or completed.stdout.strip() or "Unknown error."
            runner_errors.append(f"{python_executable}: {error_output}")
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)

    raise RuntimeError(" | ".join(runner_errors) or "No working Python runtime found for ML prediction.")


def predict_uploaded_image(uploaded_file):
    try:
        image_bytes, suffix = _read_uploaded_file_bytes(uploaded_file)
        preprocess_image_bytes(image_bytes)
    except Exception as exc:
        return {
            "label": "Invalid image",
            "confidence": 0.0,
            "asf_confidence": 0.0,
            "is_valid_image": False,
            "message": f"Could not read the uploaded image: {exc}",
            "raw_scores": [],
        }

    try:
        return _predict_with_current_runtime(image_bytes)
    except Exception as current_runtime_error:
        try:
            return _predict_with_fallback_runtime(image_bytes, suffix)
        except Exception as fallback_runtime_error:
            message = (
                "Image AI is unavailable. "
                f"Current runtime error: {current_runtime_error} "
                f"Fallback runtime error: {fallback_runtime_error}"
            )
            return {
                "label": "Model unavailable",
                "confidence": 0.0,
                "asf_confidence": 0.0,
                "is_valid_image": False,
                "message": message,
                "raw_scores": [],
            }
