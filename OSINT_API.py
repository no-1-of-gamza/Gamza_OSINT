import os
from google.cloud import vision

class TextDetector:
    def __init__(self, credentials_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.client = vision.ImageAnnotatorClient()

    def detect_text(self, image_path):
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = self.client.text_detection(image=image)
        texts = response.text_annotations
        print("Texts:")

        for text in texts:
            print(f'\n"{text.description}"')

            vertices = [
                f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
            ]

            # print("bounds: {}".format(",".join(vertices)))

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )

if __name__ == "__main__":
    credentials_path = 'groom-gamza-osint-7d145849be1a.json'
    image_path = os.path.abspath('example.jpg')
    detector = TextDetector(credentials_path)
    detector.detect_text(image_path)
