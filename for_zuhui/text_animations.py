from for_zuhui.headline import Headline
from for_zuhui.timeline import Animation


class StaggerInAnimation(Animation):
    def __init__(self, headline: Headline, staggerDelay: int):
        super().__init__()
        self.headline = headline
        self.currentTime = 0
        self.currentTextPartIndex = 0
        self.staggerDelay = staggerDelay
        self.headlineParts = self.headline.text.split(" ")
        self.headline.getDocument().set_style(
            0, len(self.headline.text), dict(color=(0, 0, 0, 0))
        )

    def paintPartsUntil(self, partIndex: int):
        limit = len(" ".join(self.headlineParts[: partIndex + 1]))
        self.headline.getDocument().set_style(
            0, limit, dict(color=self.headline._color.get_rgba())
        )

    def update(self, dt: float) -> None:
        self.currentTime += dt * 1000
        while self.currentTime >= self.staggerDelay:
            self.currentTime -= self.staggerDelay
            self.paintPartsUntil(self.currentTextPartIndex)
            self.currentTextPartIndex += 1
            if self.currentTextPartIndex >= len(self.headlineParts):
                self._completed = True
                break
