import logging

from mtcnn.mtcnn import MTCNN

logger = logging.getLogger(__name__)


class FaceDetector:
    __instance = None
    model = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(FaceDetector, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_model(self):
        if self.model is None:
            self._load_model()
        return self.model

    def _load_model(self):
        logger.info("Loading model")
        self.model = MTCNN()


def get_detector():
    return FaceDetector().get_model()
