import sys
import os
import configparser
import time
from image_to_text_API import TextDetector
from PreProcessing import Data_PreProcessing
import requests.exceptions

class Main:
    def __init__(self):
        self.load_config()

    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.file_path = self.config.get('IMAGE_FILE', 'FilePath', fallback=self.config.get('DEFAULT', 'FilePath'))
        self.credentials_path = self.config.get('CREDENTIALS_PATH', 'Credentials_path', fallback=self.config.get('DEFAULT', 'CREDENTIALS_PATH'))

    def start(self):
        self.print_welcome()
        time.sleep(0.1)
        print(f"File: {self.file_path}")
        self.OSINT()

    def print_welcome(self):
        welcome_message = r"""
            _____   ___  ___  ___ ______  ___
            |  __ \ / _ \ |  \/  ||___  / / _ \
            | |  \// /_\ \| .  . |   / / / /_\ \
            | | __ |  _  || |\/| |  / /  |  _  |
            | |_\ \| | | || |  | |./ /___| | | |
            \____/\_| |_/\_|  |_/\_____/\_| |_/
            _____  _____  _____  _   _  _____ 
            |  _  |/  ___||_   _|| \ | ||_   _|
            | | | |\ `--.   | |  |  \| |  | |  
            | | | | `--. \  | |  | . ` |  | |  
            \ \_/ //\__/ / _| |_ | |\  |  | |  
             \___/ \____/  \___/ \_| \_/  \_/  
        Please wait a moment without turning off the program until you return the results!     
        Have a nice time ~ ( ^ᴗ^ )♡ ~
        """
        print(welcome_message)
        print("------------------------------------------------------")

    def OSINT(self):    
        detector = TextDetector(self.credentials_path)
        texts_list = detector.detect_text(self.file_path)
        print(f"Detect Keywords: {', '.join(texts_list)}")
        print("------------------------------------------------------")

        for keyword in texts_list:
            data = Data_PreProcessing()
            result_add, result_road = self.process_data_with_retry(data, keyword)
            print("------------------------------------------------------")
            print(f"Keyword: {keyword}\n")

            if result_add:
                print("[Address]\n")
                for key, value in result_add.items():
                    print(f"    {key}: {value}")
            
            if result_road:
                print("\n[Road Address]\n")
                for key, value in result_road.items():
                    print(f"    {key}: {value}")
            
            print("------------------------------------------------------")


    def process_data_with_retry(self, data, keyword, max_retries=3):
        for _ in range(max_retries):
            try:
                result_add, result_road = data.start(keyword)
                return result_add, result_road
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print(f"Rate limited, retrying in a moment...")
                    time.sleep(2)
                else:
                    print(f"HTTP Error: {e}")
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        return None, None

if __name__ == "__main__":
    main = Main()
    main.start()
