import base64
from pathlib import Path
import os.path
from typing import Set
from os.path import splitext

from quart import Quart, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER: Path = Path(__file__).parent.parent / "uploads"
TEMPLATE_FOLDER: Path = Path(__file__).parent / "templates"
ALLOWED_EXTENSIONS: Set[str] = {"bmp", "png"}

app = Quart(
    __name__,
    template_folder = str(TEMPLATE_FOLDER)
)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)


def allowed_file(filename: str):
    (_, ext) = splitext(filename)
    return ext[1:] in ALLOWED_EXTENSIONS


@app.route("/box-write")
async def box_write():
    return 'unimplemented'


@app.route("/uploaded/<filename>")
async def uploaded_file(filename):
    (_, ext) = splitext(filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    with open(filepath, "rb") as fh:
        data = base64.b64encode(fh.read())
    
    return f"""
    <img src="data:image/{ext[1:]}; base64, {data.decode('utf-8')}">
    """


@app.route("/upload", methods = ["GET", "POST"])
async def upload():
    if request.method == "POST":
        if "file" not in (await request.files):
            await flash("No file part")
            return redirect(request.url)
        print(await request.files)
        file = (await request.files)["file"]

        if file.filename == "":
            await flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            await file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("uploaded_file", filename = filename))
        else:
            return "filename not allowed by extension"

    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


if __name__ == "__main__":
    app.run(debug = True, port = 8080)
    
