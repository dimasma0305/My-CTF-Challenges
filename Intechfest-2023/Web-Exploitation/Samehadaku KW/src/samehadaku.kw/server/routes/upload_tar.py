from io import BytesIO
import tarfile
from fastapi import Depends, UploadFile, APIRouter
from module.Auth import must_admin

app = APIRouter()


@app.post("/uploadtar", dependencies=[Depends(must_admin)])
async def upload_tar(file: UploadFile):
    with tarfile.open(mode="r", fileobj=BytesIO(await file.read())) as tar:
        for member in tar.getmembers():
            if member.name.startswith("/") or ".." in member.name:
                return {"message": "failed"}
        tar.extractall(path="uploads")
    return {"message": "success"}
