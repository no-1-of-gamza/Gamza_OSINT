import os
import re
from google.cloud import vision

class TextDetector:
    def __init__(self, credentials_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.client = vision.ImageAnnotatorClient()

    def is_numeric(self, text):
        # 문자열이 숫자로만 이루어져 있는지 확인
        return text.isdigit()

    def extract_korean_text(self, text):
        # 한글, 띄어쓰기, 숫자를 포함한 텍스트 추출하는 정규식 패턴 적용
        korean_text = re.sub(r"[^ㄱ-ㅣ가-힣\s0-9]", "", text)
        return korean_text

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
                korean_lines = [line for line in korean_lines if line and not self.is_numeric(line)]  # 빈 줄 및 숫자로만 이루어진 텍스트 제외
                korean_lines = [line.replace(" ", "") for line in korean_lines]  # 띄어쓰기 삭제
                texts_list.extend(korean_lines)

                vertices = [
                    f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
                ]

                # print("bounds: {}".format(",".join(vertices)))

        # 중복된 단어 제거
        texts_list = list(set(texts_list))

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
