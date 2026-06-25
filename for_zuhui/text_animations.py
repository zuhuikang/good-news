from typing import Callable

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

    def start(self) -> None:
        super().start()

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

    def start(self) -> None:
        return super().start()

    def update(self, dt: float) -> None:
        self._currentTime += dt * 1000
        if self._currentTime >= self._delay:
            self._renderable.getDocument().set_style(
                0,
                len(self._renderable.getDocument().text),
                dict(color=self._renderable.getColor().get_rgba()),
            )
            self._completed = True


class SequentialPartReplaceAnimation(Animation):
    def __init__(
        self,
        headline: Headline,
        replacer: Callable[[str], list[str]],
        replaceDelay: int,
    ) -> None:
        super().__init__()
        self._headline = headline
        self._replacer = replacer
        self._replaceDelay = replaceDelay
        self._replacementParts = replacer(headline.text)
        self._currentTime = 0
        self._parts = []
        self._currentPartIndex = 0

    def start(self) -> None:
        super().start()
        self._parts = self._headline.getDocument().text.split(" ")

    def update(self, dt: float) -> None:
        self._currentTime += dt * 1000
        while self._currentTime >= self._replaceDelay:
            self._currentTime -= self._replaceDelay
            if self._currentPartIndex >= len(self._replacementParts):
                self._completed = True
                break

            if self._currentPartIndex < len(self._parts):
                self._parts[self._currentPartIndex] = self._replacementParts[
                    self._currentPartIndex
                ]
            else:
                self._parts.append(self._replacementParts[self._currentPartIndex])

            self._headline.getDocument().text = " ".join(self._parts)
            self._currentPartIndex += 1
            if self._currentPartIndex >= len(self._replacementParts):
                self._completed = True
                break
