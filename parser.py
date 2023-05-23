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



