import logging

from flask import Flask

from model.model import get_detector
from views.views import detector_blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = "static"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
app.register_blueprint(detector_blueprint)

get_detector()


if __name__ == "__main__":
    logger.info("Starting app")
    app.run(port=8000)
