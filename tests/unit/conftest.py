import pytest
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
    return app
