import collections
import collections.abc
from pptx import Presentation





class Parser:

    def __init__(self, path):
        self.path = path
        self.presentation = Presentation(path)
        self.slides = self.presentation.slides

    def __iter__(self):
        return self.slides.__iter__()

    def get_text_from_slide(self, slide):
        text_runs = []
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                text_runs.append(paragraph.text)
        return text_runs



