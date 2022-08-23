import os
import secrets
from PIL import Image
from flaskapp import app
def save_picture(form_picture,path,output_size=None):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path,path,picture_name)
    #output_size = (300,300)
    i = Image.open(form_picture)
    if output_size:
        i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name




