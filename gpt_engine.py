# Author: Yehuda Shani
# Date: 20/5/2023
# Program description: This program is the main program that runs the GPT-3 model on powerpoint presentations.
# and writes the summary to a JSON file.

from Explainer import parser
from Explainer import gpt_prompter
import os
import asyncio
import time


def main():
    uploads_path = "content/uploads/"

    # run this code every ten seconds
    while True:
        pptx_files = [file for file in os.listdir(uploads_path) if file.endswith('.pptx')]
        for file in pptx_files:
            my_parser = parser.Parser(file)
            asyncio.run(gpt_prompter.get_gpt_answer2(my_parser, file))
            # delete the file after processing
            os.remove(os.path.join(uploads_path, file))
        print("going to sleep")
        time.sleep(10)
        print("running again")


if __name__ == "__main__":
    main()
