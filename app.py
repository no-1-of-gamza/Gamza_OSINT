import sys
import os
import configparser
import time
from image_to_text_API import TextDetector

class Main:
    def __init__(self):
        self.load_config()

    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.file_path = self.config['IMAGE_FILE'].get('FilePath', self.config['DEFAULT']['FilePath'])
        self.credentials_path = self.config['CREDENTIALS_PATH'].get('Credentials_path', self.config['DEFAULT']['CREDENTIALS_PATH'])
      
    def save_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def start(self):
        self.print_welcome()
        time.sleep(0.1)
        while True:
            command = input(">>> ").split(" ")
            if command[0] == "":
                pass

            elif command[0] == "exit":
                option = input("Are you sure to exit program? (ˊ࿁ˋ )ᐝ <yes(default)/no>: ")
                option = option.lower()
                if option == 'no' or option == 'n':
                    continue               
                sys.exit(0)

            elif command[0] == "help":
                self.help()

            elif command[0] == "start":
                self.OSINT()

                        
            else:
                print("\'{}\' is invalid command.\n".format(" ".join(command)))
                self.help()

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
                                                                                                                                                                                                                                                                  
        To know how to use, use 'help' command.
        Have a nice time ~ ( ^ᴗ^ )♡ ~
        """
        print(welcome_message)

    def exit(self):
        sys.exit(0)        
        
    def help(self):
        help = {
            "start": "Identify location information based on the text in the image.",
        }

        print("usage:", end="\n\n")
        for command in help.keys():
            print("{0:35s}\t{1:s}".format(command, help[command]))
        print()
    
    def OSINT(self):
        detector = TextDetector(self.credentials_path)
        texts_list = detector.detect_text(self.file_path)

        for keyword in texts_list:
            data += self.google.start(keyword)
            data += self.naver.start(keyword)   

            for d in data:
                content = self.page_crawler.start(d["url"])
                d["content"] = content
                time.sleep(3) 
        self.driver.close()
        
        return data


if __name__ == "__main__":
    main = Main()
    main.start()