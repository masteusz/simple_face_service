import io
import json
import logging

import cv2
import numpy as np
from flask import Flask, render_template, request, redirect
from werkzeug.datastructures import FileStorage

from model import model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".jpeg"]


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            return redirect(request.url)

    return render_template("index.html")


def detect_faces(filestream):
    detector = model.get_model()
    if type(filestream) == FileStorage:
        imgstream = filestream.stream
    else:
        imgstream = io.BytesIO(filestream)
    image = cv2.imdecode(np.fromstring(imgstream.read(), np.uint8), 1)
    return detector.detect_faces(image)


@app.route("/api/detect", methods=["POST"])
def detect_face():
    return json.dumps(detect_faces(request.data))


if __name__ == "__main__":
    app.run()
