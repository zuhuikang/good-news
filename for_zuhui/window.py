from typing import List

from pyglet.gl import glClearColor
from pyglet.window import Window as PygletWindow
from pyglet.text.layout import TextLayout

from for_zuhui.headline import Headline
from for_zuhui.logic import Color, Renderable


class Window:
    def __init__(
        self,
        content: List[Renderable],
        width=800,
        height=500,
        caption="Window",
        clearColor: Color = Color(),
        resizable=True,
    ):
        self.window = PygletWindow(width, height, caption=caption, resizable=resizable)
        self.clearColor = clearColor.get_normalized()
        self.window.push_handlers(self)
        self.content = content

    def on_draw(self):
        glClearColor(*self.clearColor.values())
        self.window.clear()
        for item in self.content:
            item.render()

    def on_resize(self, width, height):
        pass

    def on_key_press(self, symbol, modifiers):
        pass
