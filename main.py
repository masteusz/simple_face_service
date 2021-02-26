import io
import json
import logging
import os

import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from model import model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = "static"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if not check_image(image):
                redirect(request.url)
            filename = secure_filename(image.filename)
            logger.info("Successfully uploaded image")
            cvimage = convert_to_cv_image(image)
            faces = detect_faces(cvimage)
            faceimg = paint_faces(cvimage, faces)
            cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], filename), faceimg)
            return render_template("index.html", filename=filename)
    if request.method == "GET":
        return render_template("index.html")


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(
        url_for(
            "upload_image", filename=os.path.join(app.config["UPLOAD_FOLDER"], filename)
        ),
        code=301,
    )


def check_image(img):
    if img.filename == "":
        logger.warning("No filename")
        return False
    if not allowed_extension(img.filename):
        logger.warning("Extension not allowed")
        return False
    return True


def allowed_extension(filename):
    if "." not in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def detect_faces(img):
    detector = model.get_model()
    return detector.detect_faces(img)


def paint_faces(img, face_col):
    image = img.copy()
    for face in face_col:
        x1, y1, width, height = face.get("box")
        cv2.rectangle(
            image, (x1, y1), (x1 + width, y1 + height), (0, 255, 255), thickness=3
        )
    return image


def convert_to_cv_image(fstrm):
    if type(fstrm) == FileStorage:
        imgstream = fstrm.stream
    else:
        imgstream = io.BytesIO(fstrm)
    return cv2.imdecode(np.fromstring(imgstream.read(), np.uint8), 1)


@app.route("/api/detect", methods=["POST"])
def detect_face():
    image = convert_to_cv_image(request.data)
    return json.dumps(detect_faces(image))


if __name__ == "__main__":
    app.run()
