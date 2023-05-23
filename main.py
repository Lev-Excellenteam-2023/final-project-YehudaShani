import parser

parser = parser.Parser("asyncio-intro.pptx")
for slide in parser.slides:
    print(slide.__dict__)