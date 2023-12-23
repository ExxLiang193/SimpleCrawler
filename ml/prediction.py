from dataclasses import dataclass
from typing import Dict


@dataclass
class Prediction:
    label_name: str
    confidence: float

    def to_json(self) -> Dict:
        return {"label_name": self.label_name, "confidence": round(self.confidence, 3)}
