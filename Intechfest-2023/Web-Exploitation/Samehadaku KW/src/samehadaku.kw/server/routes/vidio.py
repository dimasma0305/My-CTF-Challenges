import glob
from fastapi import APIRouter, Depends
from module.Auth import authorize_user

app = APIRouter()


@app.get("/get/video", dependencies=[Depends(authorize_user)])
async def get_vidio():
    video_formats = ["mp4", "avi", "mov", "mkv"]
    video_paths = []
    for ext in video_formats:
        pattern = f"uploads/*.{ext}"
        for filepath in glob.glob(pattern):
            video_paths.append(filepath)
    return {"video_paths": video_paths}
