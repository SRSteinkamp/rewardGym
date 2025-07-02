from typing import Tuple

from psychopy.visual import TextStim

from ..display_base import BaseStimulus
from .translators import apply_psychopy_updates


class TextStimulusPsychoPy(BaseStimulus):
    """
    A stimulus class for text display in psychopy.
    """

    def __init__(
        self,
        label: str,
        text: str,
        position: Tuple[float, float] = None,
        name: str = "TextStimulus",
        text_color: str = "white",
        visible: bool = True,
        autodraw: bool = False,
    ):
        """
        Stimulus class for text displays.

        Parameters
        ----------
        duration : float
            Duration of the stimulus presentation.
        text : str
            The text that should be displayed on the screen.
        position : Tuple[float, float], optional
            Where to display the text (by default in px), by default None
        name : str, optional
            name of the object, will be used for logging, by default None
        text_color : str, optional
            Color of the text string, by default "white"
        """

        super().__init__(name=name, label=label, visible=visible, autodraw=autodraw)

        self.text = text
        self.position = position
        self.text_color = text_color

    def _backend_setup(self, window):
        """
        Implement this method to create the actual backend stimulus object.
        """
        pass

        self.textStim = TextStim(
            win=window,
            name=self.label,
            text=self.text,
            color=self.text_color,
            pos=self.position,
        )

    def _backend_draw(self):
        """
        Call the backend's draw method.
        """
        self.textStim.draw()

    def _backend_update(self, **kwargs):
        """
        Call the backend's draw method.
        """
        apply_psychopy_updates(self.textStim, **kwargs)
