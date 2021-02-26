import logging

from mtcnn.mtcnn import MTCNN

logger = logging.getLogger(__name__)

model = None


def get_model():
    global model
    if model is None:
        _load_model()
    return model


def _load_model():
    logger.info("Loading model")
    global model
    model = MTCNN()


def detect_faces(img):
    detector = get_model()
    return detector.detect_faces(img)
