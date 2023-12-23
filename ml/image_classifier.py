from typing import List, Tuple

import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms


class ImageClassifier:
    transformer = transforms.Compose(
        [
            transforms.Resize(256, antialias=True),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    def __init__(self, classifier: nn.Module) -> None:
        classifier.eval()
        self._model: nn.Module = classifier

    def predict(self, image: Image.Image, top_n: int) -> List[Tuple[int, float]]:
        image_tensor: torch.Tensor = self.transformer(image)
        image_tensor_batch: torch.Tensor = torch.unsqueeze(image_tensor, dim=0)

        prediction: torch.Tensor = self._model(image_tensor_batch)

        _, indices = torch.sort(prediction, descending=True)
        percentages = nn.functional.softmax(prediction, dim=1)[0] * 100
        return [(i, percentages[i].item()) for i in indices[0][:top_n]]
