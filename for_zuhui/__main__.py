import pyglet
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from for_zuhui.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from for_zuhui.headline import Headline
from for_zuhui.logic import Color, loadHeadlinesWithSource
from for_zuhui.sourceline import SourceLine
from for_zuhui.window import Window

print("Starting the application...")

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")

headlines = loadHeadlinesWithSource()
primaryColor = Color(0.156, 0.233, 0.920, 1)

headlinePing = Headline(
    headline=headlines[0]["title"],
    color=primaryColor.get_complementary(),
    renderWidth=WINDOW_WIDTH - 300,
)
headlinePong = Headline(
    headline=headlines[0]["title"], color=primaryColor, renderWidth=WINDOW_WIDTH - 300
)

sourcelinePing = SourceLine(
    headlines[0]["source"], color=primaryColor.get_complementary()
)


ping = Window(
    [headlinePing, sourcelinePing],
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    "ping",
    primaryColor,
    resizable=True,
)
pong = Window(
    [headlinePong],
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    "pong",
    primaryColor.get_complementary(),
    resizable=True,
)


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / 60.0)  # at 60fps
pyglet.app.run()
