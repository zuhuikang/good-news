from pyglet.text.document import FormattedDocument
from pyglet.text.layout import TextLayout

from for_zuhui.constants import FONT_NAME, SOURCE_FONT_SIZE, WINDOW_WIDTH
from for_zuhui.logic import Color, Renderable


class SourceLine(Renderable):
    def __init__(self, source: str, color: Color):
        self._color = color
        self._sourceDoc = FormattedDocument(source)
        self._sourceTextLayout = TextLayout(self._sourceDoc)
        self._sourceTextLayout.x = WINDOW_WIDTH // 2
        self._sourceTextLayout.y = 70
        self._sourceTextLayout.anchor_x = "center"
        self._sourceTextLayout.anchor_y = "bottom"

        self._sourceDoc.set_style(
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
        return self._sourceTextLayout.draw()

    def resize(self, width: int, height: int) -> None:
        self._sourceTextLayout.x = width // 2
        self._sourceTextLayout.y = 70

    def getLayout(self):
        return self._sourceTextLayout

    def getDocument(self):
        return self._sourceDoc

    def getColor(self):
        return self._color
