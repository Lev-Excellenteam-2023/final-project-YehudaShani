import parser
import gpt_prompter
import asyncio

parser = parser.Parser("asyncio-intro.pptx")

asyncio.run(gpt_prompter.get_gpt_answer(parser))
