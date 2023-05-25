# Author: Yehuda Shani
# Date: 20/5/2021
# Program description: This program is the main program that runs the GPT-3 model on powerpoint presentations.
# and writes the summary to a JSON file.

import parser
import gpt_prompter
import asyncio
import glob


def main():
    for file in glob.glob("*.pptx"): # iterate over all the pptx files in the current directory
        my_parser = parser.Parser(file)
        asyncio.run(gpt_prompter.get_gpt_answer(my_parser, file))


if __name__ == "__main__":
    main()
