from flask import current_app
import os
import secrets
from PIL import Image


def save_picture(picture):
    random_name = secrets.token_hex(8)
    _, file_ext = os.path.splitext(picture.filename)
    picture_name = random_name + file_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_name)

    output_size = (125, 125)
    image = Image.open(picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_name