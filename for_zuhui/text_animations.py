from typing import Callable

from spacy import tokens

from for_zuhui.headline import Headline
from for_zuhui.logic import Renderable
from for_zuhui.timeline import Animation


class StaggerInAnimation(Animation):
    def __init__(self, headline: Headline, staggerDelay: int):
        super().__init__()
        self._headline = headline
        self._staggerDelay = staggerDelay

    def paintPartsUntil(self, partIndex: int):
        limit = len(" ".join(self._headlineParts[: partIndex + 1]))
        self._headline.getDocument().set_style(
            0, limit, dict(color=self._headline.getColor().get_rgba())
        )

    def start(self) -> None:
        super().start()
        self._currentTime = 0
        self._currentTextPartIndex = 0
        self._headlineParts = self._headline.text.split(" ")
        self._headline.getDocument().set_style(
            0, len(self._headline.text), dict(color=(0, 0, 0, 0))
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

    def start(self) -> None:
        super().start()
        self._currentTime = 0
        self._renderable.getDocument().set_style(
            0, len(self._renderable.getDocument().text), dict(color=(0, 0, 0, 0))
        )

    def reset(self) -> None:
        super().reset()
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

        self._currentTime = 0
        self._parts = []
        self._currentPartIndex = 0
        self._mergesNeeded = 0

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


class ToSpecificPartsAnimation(Animation):
    def __init__(
        self,
        headline: Headline,
        getParts: Callable[[str], list[list[str]]],
        animDelay: int,
    ) -> None:
        super().__init__()
        self._headline = headline
        self._getParts = getParts
        self._animDelay = animDelay

    def get_desired_part_indicies(self) -> set[int]:
        desiredParts = set()
        for words in self._sentimentParts:
            n = len(words)
            for i in range(len(self._headlineParts) - n + 1):
                if self._headlineParts[i : i + n] == words:
                    for j in range(i, i + n):
                        desiredParts.add(j)

        return desiredParts

    def start(self) -> None:
        super().start()
        self._parts = []
        self._currentTime = 0
        self._hiddenIndices: set[int] = set()
        self._headlineParts = self._headline.text.split(" ")
        self._sentimentParts = self._getParts(self._headline.text)
        self._desiredIndicies = self.get_desired_part_indicies()
        self._currentPartIndex = 0
        self._parts = self._headline.getDocument().text.split(" ")
        if len(self._parts) != len(self._headlineParts):
            raise ValueError(
                "ToSpecificPartsAnimation requires the number of parts to match the headline"
            )
        self._apply_parts_styles()

    def _apply_parts_styles(self) -> None:
        document = self._headline.getDocument()

        visibleColor = self._headline.getColor().get_rgba()
        hiddenColor = (visibleColor[0], visibleColor[1], visibleColor[2], 0)

        cursor = 0
        for idx, part in enumerate(self._parts):
            start = cursor
            end = start + len(part)
            document.set_style(
                start,
                end,
                dict(color=hiddenColor if idx in self._hiddenIndices else visibleColor),
            )
            cursor = end + 1

    def _replace_part_at_index(self, idx: int, newPart: str) -> None:
        document = self._headline.getDocument()

        start = 0
        for i in range(idx):
            start += len(self._parts[i]) + 1
        end = start + len(self._parts[idx])

        document.delete_text(start, end)
        document.insert_text(start, newPart)
        self._parts[idx] = newPart

    def update(self, dt: float) -> None:
        self._currentTime += dt * 1000
        while self._currentTime >= self._animDelay:
            self._currentTime -= self._animDelay

            if self._currentPartIndex >= len(self._parts):
                self._completed = True
                break

            idx = self._currentPartIndex
            if idx in self._desiredIndicies:
                if self._parts[idx] != self._headlineParts[idx]:
                    self._replace_part_at_index(idx, self._headlineParts[idx])
            else:
                self._hiddenIndices.add(idx)

            self._apply_parts_styles()
            self._currentPartIndex += 1

            if self._currentPartIndex >= len(self._parts):
                self._completed = True
                break


class ListSentimentRatingsAnimation(Animation):
    def __init__(
        self,
        headline: Headline,
        getSentiments: Callable[[str], list[tuple[list[str], float, float, str]]],
        itemDelay: int,
    ) -> None:
        super().__init__()
        self._headline = headline
        self._getSentiments = getSentiments
        self._itemDelay = itemDelay

    def _build_sentiment_phrases(self, text: str) -> list[str]:
        sentiments = self._getSentiments(text)
        return [
            f"{' '.join(words)} {polarity:.2f}" for words, polarity, _, _ in sentiments
        ]

    def start(self) -> None:
        super().start()
        self._sentimentPhrases: list[str] = []
        self._currentTime = 0
        self._currentPhraseIndex = 0
        self._sentimentPhrases = self._build_sentiment_phrases(self._headline.text)
        document = self._headline.getDocument()

        if not self._sentimentPhrases:
            document.text = ""
            self._completed = True
            return

        document.text = self._sentimentPhrases[0]
        document.set_style(
            0,
            len(document.text),
            dict(color=self._headline.getColor().get_rgba()),
        )
        self._currentPhraseIndex = 1

    def update(self, dt: float) -> None:
        self._currentTime += dt * 1000
        while self._currentTime >= self._itemDelay:
            self._currentTime -= self._itemDelay

            if self._currentPhraseIndex >= len(self._sentimentPhrases):
                self._completed = True
                break

            document = self._headline.getDocument()
            line = self._sentimentPhrases[self._currentPhraseIndex]
            if document.text:
                document.text += "\n"
            document.text += line

            self._currentPhraseIndex += 1
            if self._currentPhraseIndex >= len(self._sentimentPhrases):
                self._completed = True
                break
