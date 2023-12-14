import os.path

from quart import Quart, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER: str = "../web/uploads"
TEMPLATE_FOLDER: str = "../web/templates"
ALLOWED_EXTENSIONS: set[str, ...] = {"bmp"}

app = Quart(
    __name__,
    template_folder = TEMPLATE_FOLDER
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename: str):
    return "." in filename and filename.split(".")[1] in ALLOWED_EXTENSIONS


@app.route("/", methods = ["GET", "POST"])
async def root():
    if request.method == "POST":
        if "file" not in request.files:
            await flash("No file part")
            return redirect(request.url)
        print(request.files)
        file = request.files["file"]

        if file.filename == "":
            await flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("uploaded_file", filename = filename))

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
    
