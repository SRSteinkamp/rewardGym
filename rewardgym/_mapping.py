import inspect

from . import reward_classes
from .psychopy_render import advanced_display, psychopy_display


def discover_classes(submodule):
    # Get all classes defined in the submodule
    classes = {
        name: cls
        for name, cls in inspect.getmembers(submodule, inspect.isclass)
        if cls.__module__ == submodule.__name__
    }

    return classes


DISPLAY_PSYCHOPY = {}

DISPLAY_PSYCHOPY.update(discover_classes(psychopy_display))
DISPLAY_PSYCHOPY.update(discover_classes(advanced_display))


REWARD_CLASSES = discover_classes(reward_classes)
