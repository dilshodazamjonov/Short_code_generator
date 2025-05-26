import qrcode
import io
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

qr_router = APIRouter()


@qr_router.get("/generate-qr/")
def generate_qr(url: str):
    # Generate the QR code
    qr_img = qrcode.make(url)

    # Save to an in-memory file
    img_io = io.BytesIO()
    qr_img.save(img_io, format='PNG')
    img_io.seek(0)

    return StreamingResponse(
        img_io,
        media_type="image/png",
        headers={
            "Content-Disposition": f"attachment; filename=qr_code.png"
        }
    )