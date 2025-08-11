import os
from typing import Optional

from app.core.config import settings


def list_storage_files() -> list[str]:
    try:
        return [os.path.join(settings.storage_dir, f) for f in os.listdir(settings.storage_dir)]
    except FileNotFoundError:
        return []


def find_file_by_id(file_id: str) -> Optional[str]:
    prefix = f"{file_id}_"
    for path in list_storage_files():
        if os.path.basename(path).startswith(prefix):
            return path
    return None


