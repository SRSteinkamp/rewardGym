import inspect
import warnings
from typing import Any, Callable, Dict, Optional, Union

import yaml


def load_yaml(yaml_path: Union[str]) -> Dict[str, Any]:
    with open(yaml_path, "r") as f:
        raw = yaml.safe_load(f)
    return raw


def load_environment_graph(filepath):
    raw_data = load_yaml(yaml_path=filepath)
    environment_graph = {}

    for state_str, value in raw_data.items():
        state = int(state_str)  # convert key to int

        # If the value is a list (e.g., [7, 8])
        if isinstance(value, list):
            environment_graph[state] = value

        # If the value is a dict
        elif isinstance(value, dict):
            processed = {}
            for k, v in value.items():
                if isinstance(v, dict) and "next" in v and "prob" in v:
                    # convert to (list, prob) tuple
                    processed[int(k)] = (v["next"], v["prob"])
                else:
                    # keep other keys like "skip"
                    processed[k] = v
            environment_graph[state] = processed

        else:
            raise ValueError(f"Unsupported value format for key {state}: {value}")

    return environment_graph


def instantiate_from_config(
    config: Any,
    class_map: Dict[str, Callable],
    inject_keys: Optional[Dict[str, Any]] = None,
    class_keys: Optional[list[str]] = None,
) -> Any:
    inject_keys = inject_keys or {}
    class_keys = class_keys or ["class", "type"]

    if isinstance(config, dict):
        key_found = next((k for k in class_keys if k in config), None)
        if key_found:
            cfg = dict(config)  # shallow copy
            cls_name = cfg.pop(key_found)
            cls = class_map.get(cls_name)
            if cls is None:
                raise ValueError(f"Unknown class/type '{cls_name}' in config")

            # Recursively instantiate any values
            for k, v in cfg.items():
                cfg[k] = instantiate_from_config(v, class_map, inject_keys, class_keys)

            # Inspect constructor signature
            sig = inspect.signature(cls.__init__)
            valid_params = set(sig.parameters.keys()) - {"self"}

            # Add only inject_keys that are valid parameters
            injected = {}
            for k, v in inject_keys.items():
                if k in cfg:
                    continue
                if k in valid_params:
                    injected[k] = v
                else:
                    warnings.warn(
                        f"Ignoring injected key '{k}' for class '{cls_name}': not in constructor",
                        UserWarning,
                    )

            return cls(**cfg, **injected)

        else:
            return {
                k: instantiate_from_config(v, class_map, inject_keys, class_keys)
                for k, v in config.items()
            }

    elif isinstance(config, list):
        return [
            instantiate_from_config(item, class_map, inject_keys, class_keys)
            for item in config
        ]

    else:
        return config


def load_objects_from_yaml(
    yaml_path: Union[str],
    class_map: Dict[str, Callable],
    inject_keys: Optional[Dict[str, Any]] = None,
    class_keys: Optional[list[str]] = None,
) -> Any:
    raw = load_yaml(yaml_path=yaml_path)
    return instantiate_from_config(raw, class_map, inject_keys, class_keys)
