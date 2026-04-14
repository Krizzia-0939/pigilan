from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "keras_model.h5"
MODEL_CACHE_PATH = BASE_DIR / "compat_model.keras"
LABELS_PATH = BASE_DIR / "labels.txt"
IMAGE_SIZE = (224, 224)
MIN_CLEAR_CONFIDENCE = 70.0


def load_class_names():
    return [
        line.strip()
        for line in LABELS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def clean_label(label):
    cleaned = str(label)
    if " " in cleaned and cleaned.split(" ", 1)[0].isdigit():
        cleaned = cleaned.split(" ", 1)[1]

    cleaned = cleaned.replace("_", " ").strip()

    normalized_map = {
        "asf suspected": "ASF Suspected",
        "no visible symptoms": "No Visible Symptoms",
        "not pig": "Not a Pig",
    }
    return normalized_map.get(cleaned.lower(), cleaned)


def preprocess_image_bytes(image_bytes):
    with Image.open(BytesIO(image_bytes)) as image:
        image = image.convert("RGB")
        image = ImageOps.fit(image, IMAGE_SIZE, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    return data


def format_prediction(prediction, class_names):
    index = int(np.argmax(prediction))
    confidence_score = float(prediction[0][index])
    cleaned_labels = [clean_label(label) for label in class_names]
    cleaned_label = cleaned_labels[index]

    asf_confidence = 0.0
    asf_index = next(
        (i for i, label in enumerate(cleaned_labels) if label.upper().startswith("ASF")),
        None,
    )
    if asf_index is not None:
        asf_confidence = float(prediction[0][asf_index]) * 100

    is_valid_image = True
    message = ""
    if cleaned_label.lower() == "not a pig":
        is_valid_image = False
        message = "Unclear photo or Not a pig detected. Please upload a valid photo of a pig."
    elif confidence_score * 100 < MIN_CLEAR_CONFIDENCE:
        is_valid_image = False
        message = "Unclear photo. Please retake a clear photo of the pig."

    return {
        "label": cleaned_label,
        "confidence": round(confidence_score * 100, 2),
        "asf_confidence": round(asf_confidence, 2),
        "is_valid_image": is_valid_image,
        "message": message,
        "raw_scores": prediction[0].tolist(),
    }


def build_legacy_teachable_machine_model(tf):
    layers = tf.keras.layers
    sequential = tf.keras.Sequential

    feature_extractor = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        alpha=0.35,
        include_top=False,
        weights=None,
    )

    model = sequential(name="sequential_4")
    model.add(layers.Input(shape=(224, 224, 3), name="sequential_1_input"))
    model.add(
        sequential(
            [
                feature_extractor,
                layers.GlobalAveragePooling2D(
                    name="global_average_pooling2d_GlobalAveragePooling2D1"
                ),
            ],
            name="sequential_1",
        )
    )
    model.add(
        sequential(
            [
                layers.Dense(
                    100,
                    activation="relu",
                    name="dense_Dense1",
                    use_bias=True,
                ),
                layers.Dense(
                    3,
                    activation="softmax",
                    name="dense_Dense2",
                    use_bias=False,
                ),
            ],
            name="sequential_3",
        )
    )
    model.load_weights(MODEL_PATH)
    return model


def _has_fresh_cached_model():
    if not MODEL_CACHE_PATH.exists():
        return False

    try:
        return MODEL_CACHE_PATH.stat().st_mtime >= MODEL_PATH.stat().st_mtime
    except OSError:
        return False


def load_or_build_model(tf):
    if _has_fresh_cached_model():
        try:
            return tf.keras.models.load_model(MODEL_CACHE_PATH, compile=False)
        except Exception:
            MODEL_CACHE_PATH.unlink(missing_ok=True)

    model = build_legacy_teachable_machine_model(tf)

    try:
        model.save(MODEL_CACHE_PATH, overwrite=True)
    except Exception:
        pass

    return model
