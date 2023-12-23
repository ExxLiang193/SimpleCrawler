from typing import TYPE_CHECKING, List

from flask import Flask, request, Response
from PIL import Image

from ml.classification_handler import ClassificationHandler
from web.instagram_image_searcher import InstagramImageSearcher

if TYPE_CHECKING:
    from ml.prediction import Prediction

IMAGE_TAG = "image"

app = Flask(__name__)


@app.route("/search/<keyword>", methods=["GET"])
def search(keyword: str):
    # Skipped input sanitation and validation for now
    image_searcher: InstagramImageSearcher = InstagramImageSearcher()
    images: List[Image.Image] = image_searcher.get_images_from_profile_posts(keyword, limit=5)

    handler: ClassificationHandler = ClassificationHandler("resnet50")
    predictions: List[List[Prediction]] = handler.analyze_images(images)

    return {
        "results": [[prediction.to_json() for prediction in image_predictions] for image_predictions in predictions]
    }


@app.route("/upload", methods=["POST"])
def upload_image():
    # Either form does not have correct key or file was not included
    if IMAGE_TAG not in request.files or request.files[IMAGE_TAG].filename == "":
        return Response("No file uploaded.", status=400)

    image: Image.Image = Image.open(request.files[IMAGE_TAG]).convert("RGB")
    handler: ClassificationHandler = ClassificationHandler("resnet50")
    predictions: List[List[Prediction]] = handler.analyze_images([image])

    return {
        "results": [[prediction.to_json() for prediction in image_predictions] for image_predictions in predictions]
    }
