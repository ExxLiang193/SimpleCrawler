# SimpleCrawler

## Setup

Requires: **python-3.10+**

Create virtual environment:
```bash
pip install virtualenv
virtualenv -p python3 venv3
source venv3/bin/activate
```

Install supplementary libraries:
```bash
pip install -r requirements.txt
```

## Starting the server

```bash
flask --app server run --port=5001
```

## APIs

`@app.route("/search/<keyword>", methods=["GET"])`
- `keyword` is an existing/nonexisting IG handle.

Uses the `keyword` for searching the specific IG profile. If the profile does not exist, returns 0 results. Downloads up to 5 latest images from the IG profile and performs image classification on each image. Cleans up downloads as well.

`@app.route("/upload", methods=["POST"])`
- Accepts `multipart/form-data` for image upload.
- Must set form key as `image`.

Expects an image to be uploaded via the request. If image is not found, responds with `400` error code. Otherwise, performs image classification on the uploaded image. Does not save image.

**All responses** (for up to 5 images):
- *List*
  - *List*
    - *Dict*
      - *Key*: `"confidence"`, *Value*: `float`
        - Confidence of classification result.
      - *Key*: `"label_name"`, *Value*: `str`
        - Name of classified item.

## Testing

- `keyword`: google, abc.def
- Wrong form key, no image, no form
