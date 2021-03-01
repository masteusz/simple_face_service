import json
import logging
import os
from io import BytesIO

import cv2
from flask import Blueprint, render_template, request, current_app, abort
from werkzeug.utils import secure_filename

from model.model import get_detector
from utils import convert_to_cv_image, check_image, paint_faces

detector_blueprint = Blueprint("detector_blueprint", __name__)

logger = logging.getLogger(__name__)


@detector_blueprint.route("/", methods=["GET", "POST"])
def web_faces():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if not check_image(image.stream):
                abort(415)
            filename = secure_filename(image.filename)
            logger.info("Successfully uploaded image")
            cvimage = convert_to_cv_image(image)
            model = get_detector()
            faces = model.detect_faces(cvimage)
            faceimg = paint_faces(cvimage, faces)
            cv2.imwrite(
                os.path.join(current_app.config["UPLOAD_FOLDER"], filename), faceimg
            )
            return render_template("index.html", filename=filename)
    if request.method == "GET":
        return render_template("index.html")


@detector_blueprint.route("/api/detect", methods=["POST"])
def detect_face():
    """
    REST API returning list of detected features: bounding boxes for each face and eyes, nose, mouth positions.
    :return:
    """
    logger.info("Detecting faces")
    if len(request.data) == 0:
        logger.error("No data received")
        abort(415)
    if not check_image(BytesIO(request.data)):
        logger.error("Extension not allowed")
        abort(415)
    image = convert_to_cv_image(request.data)
    model = get_detector()
    res = model.detect_faces(image)
    logger.info(f"Found {len(res)} faces in the image")
    return json.dumps(res)
