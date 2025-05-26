# main.py or routes.py

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.models import ShortUrl
from app.schemas import *
import string, random
from app.auth_routers import *
from app.database import *
from app.qr_code import qr_router
from app.routers.admin import router

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth_router)
app.include_router(qr_router)
app.include_router(router=router)




def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits  # base62
    return ''.join(random.choices(characters, k=length))


@app.post('/shorten', response_model=URLResponse)
def create_short_url(
    request: URLRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(ShortUrl).filter_by(original_url=str(request.original_url), owner_id=current_user.id).first()
    if existing:
        return {"short_url": f"http://127.0.0.1:8001/{existing.short_code}"}

    short_code = generate_short_code()
    while db.query(ShortUrl).filter_by(short_code=short_code).first():
        short_code = generate_short_code()

    new_url = ShortUrl(
        original_url=str(request.original_url),
        owner_id=current_user.id,
        short_code=short_code,
        created_at=datetime.utcnow(),
        visited_count=0
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {"short_url": f"http://127.0.0.1:8001/{short_code}"}


@app.get('/{short_code}')
def get_short_url(short_code: str, db: Session = Depends(get_db)):
    entry_url = db.query(ShortUrl).filter_by(short_code=short_code).first()
    if not entry_url:
        raise HTTPException(status_code=404, detail="Short url not found")

    entry_url.visited_count += 1
    db.commit()

    return RedirectResponse(url=entry_url.original_url)


@app.get('/analytics/{short_code}')
def get_short_code_analytics(
    short_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry_url = db.query(ShortUrl).filter_by(short_code=short_code).first()
    if not entry_url:
        raise HTTPException(status_code=404, detail="Short URL not found for analytics")

    if entry_url.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this short URL's analytics")

    return {
        "short_url": f"http://127.0.0.1:8001/{short_code}",
        "original_url": entry_url.original_url,
        "visited_count": entry_url.visited_count,
        "created_at": entry_url.created_at.isoformat() if entry_url.created_at else None
    }










