import io
import logging

import cv2
import numpy as np
from flask import current_app
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)


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
    if ext.upper() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def paint_faces(img, face_col, confidence_threshold=0.95, fade=False):
    image = img.copy()
    if fade:
        image = cv2.addWeighted(np.ones_like(image) * 255, 0.2, image, 0.8, 0.0)
    for face in face_col:
        conf = face.get("confidence")
        if conf < confidence_threshold:
            continue
        x1, y1, width, height = face.get("box")
        cv2.rectangle(
            image, (x1, y1), (x1 + width, y1 + height), (0, 0, 255), thickness=3
        )
    return image


def convert_to_cv_image(fstrm):
    if type(fstrm) == FileStorage:
        imgstream = fstrm.stream
    else:
        imgstream = io.BytesIO(fstrm)
    return cv2.imdecode(np.fromstring(imgstream.read(), np.uint8), 1)
