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
    def __init__(self, headline: str, color: Color, renderWidth: int):
        self.headlineDoc = FormattedDocument(headline)
        self.headlineTextLayout = TextLayout(
            self.headlineDoc, width=renderWidth, multiline=True
        )
        self.headline = headline
        self.color = color

        self.headlineDoc.set_style(
            0,
            len(headline),
            dict(
                color=color.get_rgba(),
                font_name=FONT_NAME,
                font_size=HEADLINE_FONT_SIZE,
                align="center",
            ),
        )
        self.headlineTextLayout.x = WINDOW_WIDTH // 2
        self.headlineTextLayout.y = WINDOW_HEIGHT // 2
        self.headlineTextLayout.anchor_x = "center"
        self.headlineTextLayout.anchor_y = "center"

    def render(self):
        return self.headlineTextLayout.draw()

    def resize(self, width: int, height: int) -> None:
        self.headlineTextLayout.x = width // 2
        self.headlineTextLayout.y = height // 2
        self.headlineTextLayout.width = width - 300

    def getLayout(self):
        return self.headlineTextLayout

    def getDocument(self):
        return self.headlineDoc
