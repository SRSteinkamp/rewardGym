from copy import deepcopy

import yaml


def load_display_yaml(yaml_path: str):
    with open(yaml_path, "r") as f:
        raw = yaml.safe_load(f)

    stimuli = raw.get("stimuli", {})
    templates = raw.get("templates", {})
    episodes_raw = raw.get("episodes", [])

    episodes = []
    for ep in episodes_raw:
        base = deepcopy(templates.get(ep["use"], {}))
        base.update(
            {
                k: v
                for k, v in ep.items()
                if k not in ["use", "overrides", "hooks", "name"]
            }
        )

        if "overrides" in ep:
            _deep_update(base, ep["overrides"])

        episode = {
            "name": ep["name"],
            "stimuli": stimuli,
            "hooks": ep.get("hooks", []),
            **base,
        }
        episodes.append(episode)

    return episodes


def _deep_update(d: dict, u: dict):
    """Recursively updates dict `d` with dict `u`"""
    for k, v in u.items():
        if isinstance(v, dict) and isinstance(d.get(k), dict):
            _deep_update(d[k], v)
        else:
            d[k] = v
