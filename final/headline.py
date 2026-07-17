from pyglet.text.document import FormattedDocument
from pyglet.text.layout import TextLayout

from for_zuhui.constants import (
    FONT_NAME,
    HEADLINE_FONT_SIZE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from for_zuhui.logic import Color, Renderable


class Headline(Renderable):
    def __init__(self, text: str, color: Color, renderWidth: int):
        self._headlineDoc = FormattedDocument(text)
        self._headlineTextLayout = TextLayout(
            self._headlineDoc, width=renderWidth, multiline=True
        )
        self._text = text
        self._color = color

        self._headlineDoc.set_style(
            0,
            len(text),
            dict(
                color=color.get_rgba(),
                font_name=FONT_NAME,
                font_size=HEADLINE_FONT_SIZE,
                align="center",
            ),
        )
        self._headlineTextLayout.x = WINDOW_WIDTH // 2 #여기에서 resize값으로 다시 수정.+는 위로 올라가는거
        self._headlineTextLayout.y = WINDOW_HEIGHT // 2 + 50#여기에서 resize값으로 다시 수정.
        self._headlineTextLayout.anchor_x = "center"
        self._headlineTextLayout.anchor_y = "center"

    def render(self):
        return self._headlineTextLayout.draw()

    def resize(self, width: int, height: int) -> None:
        self._headlineTextLayout.x = width // 2
        self._headlineTextLayout.y = height // 2 + 50 #여기에서 수정
        self._headlineTextLayout.width = width - 300

    @property
    def text(self):
        return self._text

    def reset(self, text: str, color: Color):
        self._text = text
        self._color = color
        self._headlineDoc.text = text
        self._headlineDoc.set_style(
            0,
            len(text),
            dict(
                color=color.get_rgba(),
                font_name=FONT_NAME,
                font_size=HEADLINE_FONT_SIZE,
                align="center",
            ),
        )

    def getLayout(self):
        return self._headlineTextLayout

    def getDocument(self):
        return self._headlineDoc

    def getColor(self) -> Color:
        return self._color
