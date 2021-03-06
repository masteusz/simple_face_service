import logging
from pathlib import Path

from flask import Flask

from config import config
from model.model import get_detector
from views.views import detector_blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
app.secret_key = config.get("secret_key", "secret")
app.config["UPLOAD_FOLDER"] = config.get("upload_folder", "static")
app.config["MAX_CONTENT_LENGTH"] = config.get("max_content_length", 16 * 1024 * 1024)
app.config["ALLOWED_IMAGE_EXTENSIONS"] = config.get(
    "allowed_image_extensions", ["JPEG", "JPG", "PNG"]
)
app.config["CONFIDENCE"] = config.get("default_confidence", 0.90)
app.register_blueprint(detector_blueprint)

# Creating upload folder in case it doesn't exist
Path(app.config["UPLOAD_FOLDER"]).mkdir(exist_ok=True)

# Preloading model
get_detector()

if __name__ == "__main__":
    logger.info("Starting app")
    app.run(port=config.get("serving_port", 8000))
