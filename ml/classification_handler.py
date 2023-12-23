import os
from typing import TYPE_CHECKING, List, Tuple

from PIL import Image

from ml.image_classifier import ImageClassifier
from ml.model_loader import ModelLoader
from ml.prediction import Prediction

if TYPE_CHECKING:
    import torch.nn as nn


class ClassificationHandler:
    LABEL_NAME_PATH = os.path.join(os.getcwd(), "ml/data/imagenet_classes.txt")

    def __init__(self, model_name: str) -> None:
        # model_name does nothing for now
        model: nn.Module = ModelLoader.instance()
        self._image_classifier: ImageClassifier = ImageClassifier(model)
        self._labels: List[str] = self._load_label_names(self.LABEL_NAME_PATH)

    def _load_label_names(self, path: str) -> List[str]:
        with open(path) as f:
            classes = [line.strip() for line in f.readlines()]
        return classes

    def analyze_images(self, images: List[Image.Image]) -> List[List[Prediction]]:
        results = list()
        for image in images:
            raw_predictions: List[Tuple[int, float]] = self._image_classifier.predict(image, 3)
            results.append([Prediction(self._labels[prediction[0]], prediction[1]) for prediction in raw_predictions])
        return results
