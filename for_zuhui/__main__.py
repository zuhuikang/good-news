import pyglet


from for_zuhui.constants import (
    ANIMATIONS_DELAY,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    WORD_ANIMATION_DELAY,
)
from for_zuhui.headline import Headline
from for_zuhui.logic import (
    Color,
    loadHeadlinesWithSource,
)
from for_zuhui.nlp_processors import (
    getNLPIsStop,
    getNLPLemma,
    getNLPPos,
    getNLPSentiment,
    getNLPShape,
    getNLPTag,
    getSentimentTexts,
)
from for_zuhui.sourceline import SourceLine
from for_zuhui.text_animations import (
    ListSentimentRatingsAnimation,
    SequentialPartReplaceAnimation,
    ShowRenderableAnimation,
    StaggerInAnimation,
    ToSpecificPartsAnimation,
)
from for_zuhui.text_modifiers import clearText, displayTextPolarity
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

# all delays are in milliseconds (1000 ms = 1 second)

timeline = Timeline()
timeline.wait(1000)
timeline.addAnimation(
    ParallelAnimations(
        [StaggerInAnimation(headlinePing, 250), StaggerInAnimation(headlinePong, 250)]
    )
)
timeline.addAnimation(ShowRenderableAnimation(sourcelinePing, 250))
timeline.wait(ANIMATIONS_DELAY)
timeline.addAnimation(
    SequentialPartReplaceAnimation(headlinePong, getNLPShape, WORD_ANIMATION_DELAY)
)
timeline.wait(ANIMATIONS_DELAY)
timeline.addAnimation(
    SequentialPartReplaceAnimation(headlinePong, getNLPLemma, WORD_ANIMATION_DELAY)
)
timeline.wait(ANIMATIONS_DELAY)
timeline.addAnimation(
    SequentialPartReplaceAnimation(headlinePong, getNLPPos, WORD_ANIMATION_DELAY)
)
timeline.wait(ANIMATIONS_DELAY)
timeline.addAnimation(
    SequentialPartReplaceAnimation(headlinePong, getNLPTag, WORD_ANIMATION_DELAY)
)
timeline.wait(ANIMATIONS_DELAY)
timeline.addAnimation(
    SequentialPartReplaceAnimation(headlinePong, getNLPIsStop, WORD_ANIMATION_DELAY)
)
timeline.wait(ANIMATIONS_DELAY)

# the False makes sure that the final resulting phrase has the same length as the original phrase
# this is needed so that the ToSpecificPartsAnimation can work properly, since it relies on the length of the original phrase to determine which parts to replace
timeline.addAnimation(
    SequentialPartReplaceAnimation(
        headlinePong, [getNLPShape, getNLPLemma], WORD_ANIMATION_DELAY, False
    )
)
timeline.wait(ANIMATIONS_DELAY)
timeline.addAnimation(
    ToSpecificPartsAnimation(headlinePong, getSentimentTexts, WORD_ANIMATION_DELAY)
)
timeline.wait(ANIMATIONS_DELAY)
timeline.addAnimation(
    ListSentimentRatingsAnimation(headlinePong, getNLPSentiment, WORD_ANIMATION_DELAY)
)
timeline.wait(ANIMATIONS_DELAY)
timeline.action(lambda: displayTextPolarity(headlinePong))
timeline.wait(ANIMATIONS_DELAY)
timeline.action(lambda: clearText(headlinePong))


def loop(dt: float) -> None:
    timeline.update(dt)


pyglet.clock.schedule_interval(loop, 1 / 60.0)  # at 60fps
pyglet.app.run()
