import os
import random
import shutil
import tempfile


def temppath_create(pathname_prefix="", pathname="", random_length=8) -> str:
    if not pathname:
        pathname = "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(random_length))

    if pathname_prefix:
        pathname = f"{pathname_prefix}{pathname}"

    full_path = os.path.join(tempfile.gettempdir(), pathname)
    os.makedirs(full_path, exist_ok=True)

    return full_path


def temppath_delete(path):
    if not os.path.isdir(path):
        return
    shutil.rmtree(path)
