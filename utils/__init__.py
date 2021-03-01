import imghdr
import io
import json
import logging
import os

import cv2
import numpy as np
import yaml
from flask import current_app
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)


def check_image(img: io.BytesIO) -> bool:
    if not img:
        logger.warning("Img is None")
        return False
    ext = imghdr.what(file=img)
    if ext is None:
        return False
    if not ext.upper() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        logger.warning("Extension not allowed")
        return False
    return True


def paint_faces(
    img: np.ndarray, face_col: list, confidence_threshold=0.95, fade=False
) -> np.ndarray:
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


def convert_to_cv_image(fstrm) -> np.ndarray:
    if type(fstrm) == FileStorage:
        imgstream = fstrm.stream
    else:
        imgstream = io.BytesIO(fstrm)
    return cv2.imdecode(np.fromstring(imgstream.read(), np.uint8), 1)


def load_as_dictionary(file_path):
    with open(file_path, "rt") as info_file:
        return {
            ".yaml": lambda: yaml.safe_load(info_file.read()),
            ".json": lambda: json.load(info_file),
        }[os.path.splitext(file_path)[1]]()


def ensure_env(env_name, default_value):
    if env_name not in os.environ:
        os.environ[env_name] = default_value
