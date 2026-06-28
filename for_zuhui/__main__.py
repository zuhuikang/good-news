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
from for_zuhui.text_modifiers import clearText, displayTextPolarity, setTextColor
from for_zuhui.timeline import ParallelAnimations, Timeline
from for_zuhui.window import Window

headlines = loadHeadlinesWithSource()
primaryColor = Color()
headlineIndex = 0

headlinePing = Headline(
    text=headlines[headlineIndex]["title"],
    color=primaryColor.get_complementary(),
    renderWidth=WINDOW_WIDTH - 300,
)
headlinePong = Headline(
    text=headlines[headlineIndex]["title"],
    color=primaryColor,
    renderWidth=WINDOW_WIDTH - 300,
)

sourcelinePing = SourceLine(
    headlines[headlineIndex]["source"], color=primaryColor.get_complementary()
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

timeline = Timeline()


def animateNextHeadline():
    global headlineIndex
    headlineIndex += 1

    if headlineIndex >= len(headlines):
        pyglet.app.exit()
        return

    primaryColor = Color()
    ping.setColor(primaryColor)
    pong.setColor(primaryColor.get_complementary())
    headlinePing.reset(
        headlines[headlineIndex]["title"], primaryColor.get_complementary()
    )
    sourcelinePing.reset(
        headlines[headlineIndex]["source"], primaryColor.get_complementary()
    )
    headlinePong.reset(headlines[headlineIndex]["title"], primaryColor)
    timeline.replay()


# all delays are in milliseconds (1000 ms = 1 second)

timeline.action(lambda: setTextColor([headlinePing, headlinePong], (0, 0, 0, 0)))
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
timeline.action(animateNextHeadline)


def loop(dt: float) -> None:
    timeline.update(dt)


pyglet.clock.schedule_interval(loop, 1 / 60.0)  # at 60fps
pyglet.app.run()
