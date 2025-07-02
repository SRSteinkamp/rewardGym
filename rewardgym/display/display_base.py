from abc import ABC, abstractmethod
from typing import Dict

from .handling import check_timing


class BaseStimulus(ABC):
    def __init__(self, name: str, label: str, **kwargs):
        self.name = name
        self.params = kwargs
        self.visible = False
        self.active = False
        self.label = label
        self.autodraw = False

    def setup(self, **kwargs):
        """
        One-time setup with the backend environment (e.g., window, screen).
        """
        self._backend_setup(**kwargs)

    @abstractmethod
    def _backend_setup(self, **kwargs):
        """
        Implement this method to create the actual backend stimulus object.
        """
        pass

    def update(self, **kwargs):
        """
        Update properties such as position, opacity, text, etc.
        Called during runtime or by hooks.
        """
        self.params.update(kwargs)
        self._backend_update(**kwargs)

    @abstractmethod
    def _backend_update(self, **kwargs):
        """
        Actually apply updates to the backend object.
        """
        pass

    def draw(
        self, current_time: float, onset: float, duration: float, episode: Dict = None
    ):
        """
        Decide whether to draw the object at this frame.
        """
        if not self.active:
            if check_timing(onset, current_time, episode=episode, mod_time=0):
                self.start_time = current_time
                self.active = True

        if self.active:
            if not check_timing(
                duration, current_time, episode=episode, mod_time=self.start_time
            ):
                self._backend_draw()
            else:
                self.active = False

    @abstractmethod
    def _backend_draw(self):
        """
        Call the backend's draw method.
        """
        pass

    def reset(self):
        """
        Optional: Reset any transient state between episodes.
        """
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} name='{self.name}'>"
