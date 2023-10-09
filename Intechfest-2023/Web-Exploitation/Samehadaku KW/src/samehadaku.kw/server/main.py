import glob
import importlib
from pathlib import Path as Pathlib
from fastapi import FastAPI, HTTPException, Response
from module.errorhandler import add_error_handler
from module.sanitizer import sanitize_path

app = FastAPI()


for module_filename in glob.glob("./routes/*"):
    if module_filename.endswith(".py"):
        module_name = f"routes.{module_filename.split('/')[-1][:-3]}"
        module = importlib.import_module(module_name)
        app.include_router(module.app)

add_error_handler(app)


@app.get("/uploads/{path:path}")
async def static_file(path: str):
    if (filepath := (Pathlib("uploads")/sanitize_path(path))).exists():
        return Response(filepath.read_bytes())
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/healthcheck")
async def health_check():
    return {"message": "ok"}
