# funtionality for writing the output to a JSON file

import json
import os
from pathlib import Path

outputs_root = "content/outputs/"

class FileWriter:
    """
    A class that writes the output to a JSON file.
    """

    def __init__(self, file_name):
        self.file_path = os.path.join(os.getcwd(), outputs_root, file_name.split('.')[0] + ".json")
        self.file = open(self.file_path, "w")
        self.file.write("[\n")
        self.file.close()

    def write_to_file(self, slide_number, text):
        """
        Write the slide number and the text to the file.
        :param slide_number: The slide number.
        :param text: The text to write.
        :return: None
        """
        self.file = open(self.file_path, "a")
        message = {"slide_number": slide_number, "content": text}
        self.file.write(json.dumps(message))
        self.file.write(",\n")
        self.file.close()

    def close_file(self):
        """
        Close the file.
        :return: None
        """
        self.file = open(self.file_path, "a")
        self.file.write("]")
        self.file.close()
