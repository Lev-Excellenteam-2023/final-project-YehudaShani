import parser

parser = parser.Parser("asyncio-intro.pptx")
for index, slide in enumerate(parser):
    print("Slide", index)
    print("Text:", parser.get_text_from_slide(slide))