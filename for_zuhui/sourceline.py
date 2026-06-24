from pyglet.text.document import FormattedDocument
from pyglet.text.layout import TextLayout

from for_zuhui.constants import FONT_NAME, SOURCE_FONT_SIZE, WINDOW_WIDTH
from for_zuhui.logic import Color, Renderable


class SourceLine(Renderable):
    def __init__(self, source: str, color: Color):
        self.sourceDoc = FormattedDocument(source)
        self.sourceTextLayout = TextLayout(self.sourceDoc)
        self.sourceTextLayout.x = WINDOW_WIDTH // 2
        self.sourceTextLayout.y = 70
        self.sourceTextLayout.anchor_x = "center"
        self.sourceTextLayout.anchor_y = "bottom"

        self.sourceDoc.set_style(
            0,
            len(source),
            dict(
                color=color.get_rgba(),
                font_name=FONT_NAME,
                font_size=SOURCE_FONT_SIZE,
                align="center",
            ),
        )

    def render(self):
        return self.sourceTextLayout.draw()

    def resize(self, width: int, height: int) -> None:
        self.sourceTextLayout.x = width // 2
        self.sourceTextLayout.y = 70

    def getLayout(self):
        return self.sourceTextLayout
