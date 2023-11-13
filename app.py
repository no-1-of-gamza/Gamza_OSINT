import sys
import os
import configparser
import time
from OSINT_API import detect_text

class Main:
    def __init__(self):
        self.load_config()

    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.mobsf_path = self.config['MobSF'].get('MobSF', self.config['DEFAULT']['MobSF'])
        self.server_ip = self.config['SERVER'].get('ServerIP', self.config['DEFAULT']['ServerIP'])
        self.api_key = self.config['API'].get('ApiKey', self.config['DEFAULT']['ApiKey'])
        self.file_path = self.config['FILE'].get('FilePath', self.config['DEFAULT']['FilePath']).split(',')
        self.avm_name = self.config['AVM'].get('AVM_Name', self.config['DEFAULT']['AVM_Name'])
        self.frida_script_path = self.config['Frida'].get('Frida_Script', self.config['DEFAULT']['Frida_Script'])
        self.encryption_method = self.config['Encryption_method'].get('encryption_method', self.config['DEFAULT']['Encryption_method'])
        
    def save_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def start(self):
        self.print_welcome()
        self.run_mobsf()
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
                self.exit(0)

            elif command[0] == "help":
                self.help()

            elif command[0] == "detect" and len(command) > 1 and command[1] == "text":
                self.static_analysis()

                        
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
        Have a nice time ~ ( ･ᴗ･ )♡ ~
        """
        print(welcome_message)

    def exit(self):
        sys.exit(0)        
        
    def help(self):
        help = {
            "detect text": "Extract text from a picture",
        }

        print("usage:", end="\n\n")
        for command in help.keys():
            print("{0:35s}\t{1:s}".format(command, help[command]))
        print()