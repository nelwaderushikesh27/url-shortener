"""
Utility functions for URL Shortener.
"""

import string
import random
import io
import qrcode


def generate_short_code(length: int = 6) -> str:
    """Generate a random short code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def generate_qr_code(url: str) -> io.BytesIO:
    """Generate QR code for a URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer)
    buffer.seek(0)
    
    return buffer


def validate_url(url: str) -> bool:
    """Validate a URL."""
    from urllib.parse import urlparse
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_expired(expires_at) -> bool:
    """Check if a URL has expired."""
    from datetime import datetime
    
    if expires_at is None:
        return False
    
    return datetime.utcnow() > expires_at
