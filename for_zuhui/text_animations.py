from for_zuhui.headline import Headline
from for_zuhui.logic import Renderable
from for_zuhui.timeline import Animation


class StaggerInAnimation(Animation):
    def __init__(self, headline: Headline, staggerDelay: int):
        super().__init__()
        self._headline = headline
        self._currentTime = 0
        self._currentTextPartIndex = 0
        self._staggerDelay = staggerDelay
        self._headlineParts = self._headline.text.split(" ")
        self._headline.getDocument().set_style(
            0, len(self._headline.text), dict(color=(0, 0, 0, 0))
        )

    def paintPartsUntil(self, partIndex: int):
        limit = len(" ".join(self._headlineParts[: partIndex + 1]))
        self._headline.getDocument().set_style(
            0, limit, dict(color=self._headline.getColor().get_rgba())
        )

    def update(self, dt: float) -> None:
        self._currentTime += dt * 1000
        while self._currentTime >= self._staggerDelay:
            self._currentTime -= self._staggerDelay
            self.paintPartsUntil(self._currentTextPartIndex)
            self._currentTextPartIndex += 1
            if self._currentTextPartIndex >= len(self._headlineParts):
                self._completed = True
                break


class ShowRenderableAnimation(Animation):
    def __init__(self, renderable: Renderable, delay: int):
        super().__init__()
        self._renderable = renderable
        self._delay = delay
        self._currentTime = 0
        self._renderable.getDocument().set_style(
            0, len(self._renderable.getDocument().text), dict(color=(0, 0, 0, 0))
        )

    def update(self, dt: float) -> None:
        self._currentTime += dt * 1000
        if self._currentTime >= self._delay:
            self._renderable.getDocument().set_style(
                0,
                len(self._renderable.getDocument().text),
                dict(color=self._renderable.getColor().get_rgba()),
            )
            self._completed = True
