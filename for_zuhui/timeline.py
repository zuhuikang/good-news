from abc import ABC, abstractmethod
from typing import Sequence


class Timeline:
    def __init__(self):
        self.animations: list[Animation] = []
        self.currentTime = 0
        self.currentAnimationIndex = 0

    def addAnimation(self, animation: Animation):
        self.animations.append(animation)

    def wait(self, delayMs: int):
        self.addAnimation(DelayAnimation(delayMs))

    def update(self, dt):
        self.currentTime += dt

        if not self.animations:
            return
        if self.currentAnimationIndex >= len(self.animations):
            return

        currentAnim = self.animations[self.currentAnimationIndex]
        if not currentAnim.started:
            currentAnim.start()
            currentAnim.started = True

        currentAnim.update(dt)

        if currentAnim.completed:
            self.currentAnimationIndex += 1


class Animation(ABC):

    def __init__(self) -> None:
        self._completed: bool = False
        self._started: bool = False

    @property
    def started(self) -> bool:
        return self._started

    @started.setter
    def started(self, value: bool) -> None:
        self._started = value

    @property
    def completed(self) -> bool:
        return self._completed

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass


class ParallelAnimations(Animation):
    def __init__(self, animations: Sequence[Animation]) -> None:
        super().__init__()
        self.animations = animations

    def start(self) -> None:
        super().start()

    def update(self, dt: float) -> None:
        for animation in self.animations:
            if not animation.completed:
                animation.update(dt)

        if all(animation.completed for animation in self.animations):
            self._completed = True


class DelayAnimation(Animation):
    def __init__(self, delayMs: int):
        super().__init__()
        self._delayMs = delayMs
        self._currentTime = 0

    def start(self) -> None:
        return super().start()

    def update(self, dt: float) -> None:
        self._currentTime += dt * 1000
        if self._currentTime >= self._delayMs:
            self._completed = True
