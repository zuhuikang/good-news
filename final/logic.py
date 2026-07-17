from abc import ABC, abstractmethod
from pathlib import Path
from random import random
from pyglet.text.layout import TextLayout
from pyglet.text.document import FormattedDocument


class Color:
    def __init__(self, r=None, g=None, b=None, a=None):
        self.r = random() if r is None else r
        self.g = random() if g is None else g
        self.b = random() if b is None else b
        self.a = 1.0 if a is None else a

    def get_rgba(self):
        return (
            int(self.r * 255),
            int(self.g * 255),
            int(self.b * 255),
            int(self.a * 255),
        )

    def get_normalized(self):
        return {"r": self.r, "g": self.g, "b": self.b, "a": self.a}

    def get_complementary(self):
        return Color(1.0 - self.r, 1.0 - self.g, 1.0 - self.b, self.a)


class Renderable(ABC):
    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def getLayout(self) -> TextLayout:
        pass

    @abstractmethod
    def getDocument(self) -> FormattedDocument:
        pass

    @abstractmethod
    def resize(self, width: int, height: int) -> None:
        pass

    @abstractmethod
    def getColor(self) -> Color:
        pass


def loadHeadlinesWithSource():
    current_dir = Path(__file__).parent
    file_path = current_dir.parent / "headline_with_source.txt"
    with open(file_path, "r") as myTxt:
        eachLine = []
        for line in myTxt:
            if line.strip():
                eachLine.append(line.strip())

        headLines = []
        for line in eachLine:
            if "|" in line:
                title, source = line.split("|", 1)
                headLines.append({"title": title.strip(), "source": source.strip()})
            else:
                headLines.append({"title": line.strip(), "source": ""})
        return headLines