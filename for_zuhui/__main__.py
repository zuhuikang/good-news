import pyglet


from for_zuhui.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from for_zuhui.headline import Headline
from for_zuhui.logic import Color, loadHeadlinesWithSource
from for_zuhui.nlp_processors import (
    getNLPIsStop,
    getNLPLemma,
    getNLPPos,
    getNLPShape,
    getNLPTag,
)
from for_zuhui.sourceline import SourceLine
from for_zuhui.text_animations import (
    SequentialPartReplaceAnimation,
    ShowRenderableAnimation,
    StaggerInAnimation,
)
from for_zuhui.timeline import ParallelAnimations, Timeline
from for_zuhui.window import Window

headlines = loadHeadlinesWithSource()
primaryColor = Color(0.156, 0.233, 0.920, 1)

headlinePing = Headline(
    text=headlines[0]["title"],
    color=primaryColor.get_complementary(),
    renderWidth=WINDOW_WIDTH - 300,
)
headlinePong = Headline(
    text=headlines[0]["title"], color=primaryColor, renderWidth=WINDOW_WIDTH - 300
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


# timeline:
timeline = Timeline()
timeline.wait(1000)
timeline.addAnimation(
    ParallelAnimations(
        [StaggerInAnimation(headlinePing, 250), StaggerInAnimation(headlinePong, 250)]
    )
)
timeline.addAnimation(ShowRenderableAnimation(sourcelinePing, 250))
timeline.wait(2000)
timeline.addAnimation(SequentialPartReplaceAnimation(headlinePong, getNLPShape, 150))
timeline.wait(2000)
timeline.addAnimation(SequentialPartReplaceAnimation(headlinePong, getNLPLemma, 150))
timeline.wait(2000)
timeline.addAnimation(SequentialPartReplaceAnimation(headlinePong, getNLPPos, 150))
timeline.wait(2000)
timeline.addAnimation(SequentialPartReplaceAnimation(headlinePong, getNLPTag, 150))
timeline.wait(2000)
timeline.addAnimation(SequentialPartReplaceAnimation(headlinePong, getNLPIsStop, 150))


# This is the main animation loop.
def loop(dt: float) -> None:
    timeline.update(dt)


pyglet.clock.schedule_interval(loop, 1 / 60.0)  # at 60fps
pyglet.app.run()
