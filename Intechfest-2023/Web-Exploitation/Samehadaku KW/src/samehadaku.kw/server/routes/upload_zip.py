import random
import string
import subprocess
from pathlib import Path
from fastapi import UploadFile, APIRouter

app = APIRouter()
UPLOAD_PATH = Path("./uploads/")


def get_random_string(length: int = 16) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


@app.post("/uploadzip")
async def upload_zip(file: UploadFile):
    while (tmp_path := UPLOAD_PATH/get_random_string()).exists():
        pass
    while (file_path := UPLOAD_PATH/get_random_string()).exists():
        pass
    with open(tmp_path, "wb") as f:
        f.write(await file.read())
    args = ['unzip', tmp_path, '-d', file_path]
    subprocess.run(args, timeout=1)
    tmp_path.unlink()
    return {"filename": file_path}
