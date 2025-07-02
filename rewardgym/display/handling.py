import operator
from typing import Dict


def attribute_getter(item_list, cls_name, cls_attribute):
    for item in item_list:
        if item.label == cls_name:
            return item.__getattribute__(cls_attribute)

    raise ValueError(f"{cls_name} was not found in episode")


def attribute_setter(item_list, cls_name, cls_attribute, value):
    for item in item_list:
        if item.label == cls_name:
            setattr(item, cls_attribute, value)

            return None

    raise ValueError(f"{cls_name} was not found in episode")


def trigger_handler(trigger_string: str, episode: Dict):
    episode_designation, cls_name, cls_attribute = trigger_string.split(".")

    if cls_attribute not in ["started", "ended", "active"]:
        raise NotImplementedError(
            f"{cls_attribute}, is not a recognized timing attribute"
        )

    attribute = attribute_getter(episode[episode_designation], cls_name, cls_attribute)

    return attribute


# Handles onsets relative to other stimuli and periods (e.g. "periods.fix.started" if a stimulus should start
# after onset of a fixation period, or "render.stim_left.ended" to have something appear after the stimulus offset.


def check_timing(check_time, t, episode, mod_time=0):
    if isinstance(check_time, str):
        return trigger_handler(trigger_string=check_time, episode=episode)

    elif isinstance(check_time, (int, float)):
        return operator.gt(t, check_time + mod_time)

    else:
        raise ValueError("Duration needs to be a string or number")
