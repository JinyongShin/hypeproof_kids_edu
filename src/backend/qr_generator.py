"""
QR code generation for Kids Edu — 사원증용 QR.
캐릭터 카드 URL → QR 이미지(PNG) 생성.
"""

import io
import logging
import qrcode

logger = logging.getLogger(__name__)


def generate_qr_png(url: str, child_name: str = "") -> bytes:
    """URL을 QR PNG로 변환하여 bytes 반환."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#7C3AED", back_color="white")  # 보라색 QR (테마 컬러)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_qr_base64(url: str, child_name: str = "") -> str:
    """URL을 QR base64 문자열로 반환 (프론트엔드 img src용)."""
    import base64
    png_bytes = generate_qr_png(url, child_name)
    return base64.b64encode(png_bytes).decode("utf-8")
