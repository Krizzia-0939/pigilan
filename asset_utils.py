import base64
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
ASSET_DIRS = (
    ROOT_DIR / "assets",
    ROOT_DIR / "Assets",
)


def resolve_asset_path(file_name: str) -> Path:
    for asset_dir in ASSET_DIRS:
        asset_path = asset_dir / file_name
        if asset_path.exists():
            return asset_path
    return ROOT_DIR / file_name


def build_local_image_data_uri(path: Path):
    if not path.exists():
        return None

    mime_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(path.suffix.lower())

    if not mime_type:
        return None

    encoded_bytes = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded_bytes}"
