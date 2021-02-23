import io
import logging

import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
import json
from model import model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/")
def web_interface():
    return render_template("example.html", title="Welcome", username="test")


@app.route("/", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for("web_interface"))


@app.route("/api/detect", methods=["POST"])
def detect_face():
    detector = model.get_model()
    uploaded_file = request.data
    imgstream = io.BytesIO(uploaded_file)
    image = cv2.imdecode(np.fromstring(imgstream.read(), np.uint8), 1)
    data = detector.detect_faces(image)
    return json.dumps(data)


if __name__ == "__main__":
    app.run(debug=True)
