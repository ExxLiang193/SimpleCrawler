from __future__ import annotations

from typing import TYPE_CHECKING

from torchvision import models

if TYPE_CHECKING:
    import torch.nn as nn


class ModelLoader:
    _instance = None
    model_name = "model_name"

    def __new__(cls) -> nn.Module:
        # Hardcoded for resnet50 for now
        if cls.model_name is not None:
            return models.resnet50(weights=models.ResNet50_Weights.DEFAULT)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance
