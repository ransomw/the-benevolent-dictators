import base64
from pathlib import Path
import os.path
from typing import Set
from os.path import splitext
from io import BytesIO
from asyncio import Lock
import uuid

from quart import Quart, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError
import pandas as pd

UPLOAD_FOLDER: Path = Path(__file__).parent.parent / "uploads"
TEMPLATE_FOLDER: Path = Path(__file__).parent / "templates"

uploads_lock = Lock()

app = Quart(
    __name__,
    template_folder = str(TEMPLATE_FOLDER)
)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

df_filename = UPLOAD_FOLDER / "images.csv"

def _get_images_df():
    if not os.path.exists(df_filename):
        df = pd.DataFrame([], columns=["name", "filename"])
        df.to_csv(df_filename)
    df = pd.read_csv(df_filename)
    return df


async def get_images_df():
    async with uploads_lock:
        df = _get_images_df()
    return df


async def get_image(name):
    async with uploads_lock:
        df = _get_images_df()
        sel_df = df.loc[df['name'] == name]
        if len(sel_df) == 0:
            return None
        elif len(sel_df) > 1:
            raise RuntimeError("duplicate names")
        filename = sel_df.iloc[0]["filename"]
        image = Image.open(UPLOAD_FOLDER / filename)
    return image


async def get_image_names():
    async with uploads_lock:
        df = _get_images_df()
        names = df['name'].tolist()
    return names


class StoreImageException(Exception):
    pass


async def store_image(name, image: Image):
    filename = str(uuid.uuid4()) + "." + image.format.lower()
    async with uploads_lock:
        df_pre = _get_images_df()
        if any(df_pre["name"] == name):
            raise StoreImageException("duplicate name", name)
        row_series = pd.Series([name, filename], index=["name", "filename"])
        df_post = pd.concat([df_pre, row_series.to_frame().T], ignore_index=True)
        image.save(UPLOAD_FOLDER / filename)
        df_post.to_csv(df_filename)


@app.route("/uploaded")
async def uploaded():
    names = await get_image_names()
    return ("<ul>" +
            '\n'.join([
                f"<li><a href={url_for('uploaded_file', name = name)}>{name}</a></li>"
                for name in names
                ]) +
            "</ul>")


@app.route("/uploaded/<name>")
async def uploaded_file(name):
    
    image = await get_image(name)
    im_buf = BytesIO()
    image.save(im_buf, format=image.format)
    data = base64.b64encode(im_buf.getvalue())
    
    return f"""
    <img src="data:image/{image.format.lower()}; base64, {data.decode('utf-8')}">
    """


@app.route("/upload", methods = ["GET", "POST"])
async def upload():
    if request.method == "POST":
        request_form = await request.form
        request_files = await request.files
        if "file" not in request_files:
            return "No file part"
        file = request_files["file"]
        if not file or file.filename == "":
            return "No selected file"
        file_bytes = file.stream.read()
        try:
            image = Image.open(BytesIO(file_bytes))
        except UnidentifiedImageError:
            return "not an image file"
        if request_form["name"]:
            name = secure_filename(request_form["name"])
        else:
            name = secure_filename(file.filename)
        try:
            await store_image(name, image)
        except StoreImageException as ex:
            return repr(StoreImageException)
        return redirect(url_for("uploaded_file", name = name))
        
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=text name=name>
          <input type=submit value=Upload>
        </form>
        '''


if __name__ == "__main__":
    app.run(debug = True, port = 8080)
    
