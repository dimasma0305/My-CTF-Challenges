from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from module.Auth import User, authorize_user, must_admin

app = APIRouter()
templates = Jinja2Templates(directory="views")


@app.get("/", response_class=HTMLResponse)
async def home(
    res: Response,
    request: Request,
    user: User = Depends(authorize_user)
):
    config = user.config()
    context = {
        "title": "Home Page",
        "user": user,
        "theme": config['ui']['theme'],
    }
    return templates.TemplateResponse("home.html", {
        "request": request,
        "context": context
    }, headers=res.headers)


@app.get("/animelist", response_class=HTMLResponse)
async def animelist(request: Request, user: User = Depends(authorize_user)):
    config = user.config()
    context = {
        "title": "Anime List",
        "user": user,
        "theme": config['ui']['theme']
    }
    return templates.TemplateResponse("anime_list.html", {
        "request": request,
        "context": context
    })


@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, user: User = Depends(must_admin)):
    config = user.config()
    context = {
        "title": "Admin Panel",
        "user": user,
        "theme": config['ui']['theme']
    }
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "context": context
    })
