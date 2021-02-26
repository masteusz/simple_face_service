import json
import logging
import os

import cv2
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

from model.model import detect_faces
from utils import convert_to_cv_image, check_image, paint_faces

detector_blueprint = Blueprint("detector_blueprint", __name__)

logger = logging.getLogger(__name__)


@detector_blueprint.route("/upload-image", methods=["GET", "POST"])
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
            cv2.imwrite(
                os.path.join(current_app.config["UPLOAD_FOLDER"], filename), faceimg
            )
            return render_template("index.html", filename=filename)
    if request.method == "GET":
        return render_template("index.html")


@detector_blueprint.route("/display/<filename>")
def display_image(filename):
    return redirect(
        url_for(
            "upload_image",
            filename=os.path.join(current_app.config["UPLOAD_FOLDER"], filename),
        ),
        code=301,
    )


@detector_blueprint.route("/api/detect", methods=["POST"])
def detect_face():
    image = convert_to_cv_image(request.data)
    return json.dumps(detect_faces(image))
