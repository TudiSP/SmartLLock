import uuid

import qrcode
from io import BytesIO

def generate_code():
    token = uuid.uuid1()
    return token.int

def generate_QR():
    code = generate_code()

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(code)

    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer)

    return buffer.getbuffer(), code
