from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth_routers import get_current_user
from app.database import get_db
from app.models import *

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/")
def admin_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "title": "Admin Dashboard"})


@router.get("/stats")
def load_stats(request: Request):
    return templates.TemplateResponse("partials/stats.html", {"request": request})


@router.get("/users")
def user_list(request: Request, db: Session = Depends(get_db), page: int = 1, per_page: int = 10):
    offset = (page - 1) * per_page
    users = db.query(User).offset(offset).limit(per_page).all()
    total_users = db.query(User).count()
    return templates.TemplateResponse("admin_users.html", {
        "request": request,
        "users": users,
        "page": page,
        "total_pages": (total_users + per_page - 1) // per_page
    })


