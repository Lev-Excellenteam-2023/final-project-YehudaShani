# funtionality for writing the output to a JSON file

import json
import os

class FileWriter:

    def __init__(self, file_name):
        self.file_path = os.path.join(os.getcwd(), file_name + ".json")
        self.file = open(self.file_path, "w")
        self.file.write("[\n")
        self.file.close()

    def write_to_file(self, text, slide_number):
        self.file = open(self.file_path, "a")
        message = {"slide_number": slide_number, "content": text}
        self.file.write(json.dumps(message))
        self.file.write(",\n")
        self.file.close()

    def close_file(self):
        self.file = open(self.file_path, "a")
        self.file.write("]")
        self.file.close()