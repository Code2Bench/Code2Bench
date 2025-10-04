import base64
from io import BytesIO

def image_to_data_url(image) -> str:
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    encoded_img = base64.b64encode(img_byte_arr.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_img}"