import json
import os
import sys
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

from ml_model_compat import (  # noqa: E402
    format_prediction,
    load_or_build_model,
    load_class_names,
    preprocess_image_bytes,
)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: ml_compat_runner.py <image_path>")

    image_path = Path(sys.argv[1])
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    import tensorflow as tf  # noqa: E402

    model = load_or_build_model(tf)
    prediction = model.predict(
        preprocess_image_bytes(image_path.read_bytes()),
        verbose=0,
    )
    result = format_prediction(prediction, load_class_names())
    print(json.dumps(result))


if __name__ == "__main__":
    main()
