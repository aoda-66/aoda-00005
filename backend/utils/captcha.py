from io import BytesIO
import random
from PIL import Image, ImageDraw, ImageFont

captcha_store = {}

def generate_captcha() -> tuple[str, bytes]:
    width, height = 120, 40
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz0123456789'
    captcha_text = ''.join(random.choices(chars, k=4))
    
    try:
        font = ImageFont.truetype('arial.ttf', 28)
    except:
        font = ImageFont.load_default()
    
    for i, char in enumerate(captcha_text):
        x = 15 + i * 25
        y = random.randint(5, 10)
        draw.text((x, y), char, fill=(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)), font=font)
    
    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)), width=1)
    
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    captcha_id = str(random.randint(100000, 999999))
    captcha_store[captcha_id] = captcha_text.lower()
    
    return captcha_id, buffer.getvalue()

def verify_captcha(captcha_id: str, user_input: str) -> bool:
    captcha_text = captcha_store.get(captcha_id)
    if not captcha_text:
        return False
    result = captcha_text == user_input.lower()
    del captcha_store[captcha_id]
    return result