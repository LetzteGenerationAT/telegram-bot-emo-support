"""
Config script for the telegram bot. Holding an instance of the config class.
"""

import json
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class Config:
    """
    Config class for the telgram bot.
    """

    CONFIG_FILE = "config/config.json"

    def __init__(self):
        self.config = {
            "case-number": 0,
            "response-message": ""
        }

    def get_response_message(self) -> str:
        """
        Return the configured response meassage.
        """
        return self.config["response-message"]

    def set_response_message(self, message) -> None:
        """
        Configure the respons messsage.
        """
        self.config["response-message"] = message

    def next_case_number(self) -> int:
        """
        Increment and set the configured case number.
        """
        number = self.config["case-number"] + 1
        self.config["case-number"] = number
        return number

    def read_config(self) -> None:
        """
        Load the config file from json.
        """
        try:
            with open(self.CONFIG_FILE, "r", encoding="utf-8") as file:
                self.config = json.load(file)
        except FileNotFoundError as ex:
            return logging.exception(ex)

    def write_config(self) -> None:
        """"
        Save the config as json file. 
        """
        try:
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as file:
                json.dump(self.config, file, indent=4)
        except FileNotFoundError as ex:
            return logging.exception(ex)

config = Config()
config.read_config()
