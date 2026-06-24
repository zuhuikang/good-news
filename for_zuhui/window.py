from typing import List
import pyglet
from pyglet.gl import glClearColor
from pyglet.window import Window as PygletWindow


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
        for item in self.content:
            item.resize(width, height)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)
