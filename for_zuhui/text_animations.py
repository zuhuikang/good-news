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
        replacers: Callable[[str], list[str]] | list[Callable[[str], list[str]]],
        replaceDelay: int,
        replaceAsIs: bool = True,
    ) -> None:
        super().__init__()
        self._headline = headline
        self._replacers = replacers
        self._use_current_phrase = replaceAsIs
        self._replaceDelay = replaceDelay
        self._currentTime = 0
        self._parts = []
        self._currentPartIndex = 0
        self._mergesNeeded = 0

    def get_parts(self, use_current: bool = True) -> list[str]:
        if use_current:
            return self._headline.getDocument().text.split(" ")
        else:
            return self._headline.text.split(" ")

    def _build_replacement_parts(
        self, replacers: list[Callable[[str], list[str]]], use_current: bool = True
    ) -> list[str]:
        """Build replacement parts from multiple replacers using round-robin selection"""
        replacementParts: list[str] = []
        replacementOptions: list[list[str]] = []
        for replacer in replacers:
            replacementOptions.append(replacer(self._headline.text))

        originalParts = self.get_parts(use_current)
        if not replacementOptions:
            raise ValueError(
                "SequentialPartReplaceAnimation requires at least one replacer"
            )

        replacementOptionsCount = len(replacementOptions)
        goalLength = len(originalParts)

        for i in range(goalLength):
            option = replacementOptions[i % replacementOptionsCount]
            if not option:
                replacementParts.append(originalParts[i])
                continue
            replacementParts.append(option[i % len(option)])

        return replacementParts

    def start(self) -> None:
        super().start()

        if isinstance(self._replacers, list):
            self._replacementParts = self._build_replacement_parts(
                self._replacers, self._use_current_phrase
            )
        else:
            self._replacementParts = self._replacers(self._headline.text)

        self._parts = self._headline.getDocument().text.split(" ")

        # Calculate if we need to merge parts
        if len(self._parts) > len(self._replacementParts):
            self._mergesNeeded = len(self._parts) - len(self._replacementParts)

    def update(self, dt: float) -> None:
        self._currentTime += dt * 1000
        while self._currentTime >= self._replaceDelay:
            self._currentTime -= self._replaceDelay
            if self._currentPartIndex >= len(self._replacementParts):
                self._completed = True
                break

            # Merge adjacent parts if we have more parts than replacements
            if self._mergesNeeded > 0 and len(self._parts) > len(
                self._replacementParts
            ):
                if self._currentPartIndex + 1 < len(self._parts):
                    # Merge current part with next part
                    self._parts[self._currentPartIndex] = (
                        self._parts[self._currentPartIndex]
                        + " "
                        + self._parts.pop(self._currentPartIndex + 1)
                    )
                    self._mergesNeeded -= 1

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
