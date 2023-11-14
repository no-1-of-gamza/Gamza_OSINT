import os
import re
from google.cloud import vision

class TextDetector:
    def __init__(self, credentials_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.client = vision.ImageAnnotatorClient()

    def is_numeric(self, text):
        return text.isdigit()

    def extract_korean_text(self, text):
        korean_text = re.sub(r"[^ㄱ-ㅣ가-힣\s0-9]", "", text)
        return korean_text

    def remove_numeric_space(self, text):
        # 띄어쓰기가 있는 문자열 중에서 숫자로만 이루어진 부분 제거
        parts = text.split()
        cleaned_parts = [part for part in parts if not self.is_numeric(part)]
        cleaned_text = " ".join(cleaned_parts)
        return cleaned_text

    def detect_text(self, image_path):
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = self.client.text_detection(image=image)
        texts = response.text_annotations
        texts_list = []

        for text in texts:
            if text.locale.startswith("ko"):
                text_description = text.description.strip()
                lines = text_description.splitlines()
                korean_lines = [self.extract_korean_text(line) for line in lines]
                korean_lines = [line for line in korean_lines if line]  # 빈 줄 제외
                korean_lines = [self.remove_numeric_space(line) for line in korean_lines]  # 숫자로만 이루어진 부분 제거
                texts_list.extend(korean_lines)

                vertices = [
                    f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
                ]

                # print("bounds: {}".format(",".join(vertices)))

        # 빈 문자열 및 빈 리스트 제거
        texts_list = [text for text in texts_list if text]

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )

        return texts_list

if __name__ == "__main__":
    credentials_path = 'groom-gamza-osint-7d145849be1a.json'
    image_path = os.path.abspath('example.jpg')
    detector = TextDetector(credentials_path)
    texts = detector.detect_text(image_path)
    print(texts)
