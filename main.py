import parser
import gpt_prompter
import asyncio
import glob

for file in glob.glob("*.pptx"):
    parser = parser.Parser(file)
    asyncio.run(gpt_prompter.get_gpt_answer(parser, file))


