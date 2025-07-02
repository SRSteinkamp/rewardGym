from typing import Dict


def apply_psychopy_updates(stimulus_obj, updates: Dict):
    """
    Translate rewardgym generalized attributes to PsychoPy
    """
    attribute_dict = {
        "position": "pos",
        "text_color": "color",
        "autodraw": "autoDraw",
    }

    for key, value in updates.items():
        if hasattr(stimulus_obj, key):
            setattr(stimulus_obj, key, value)
        elif hasattr(stimulus_obj, attribute_dict[key]):
            setattr(stimulus_obj, attribute_dict[key], value)
        else:
            raise AttributeError(
                f"{stimulus_obj} has no property or setter for '{key}'"
            )
