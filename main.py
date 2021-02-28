import logging

from flask import Flask

from views.views import detector_blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)


if __name__ == "__main__":
    logger.info("Configuring")
    app.secret_key = "secret key"
    app.config["UPLOAD_FOLDER"] = "static"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
    logger.info("Registering blueprints")
    app.register_blueprint(detector_blueprint)
    logger.info("Starting app")
    app.run(port=8000)
