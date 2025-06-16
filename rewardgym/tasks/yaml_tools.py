import yaml


def load_environment_graph(filepath):
    with open(filepath, "r") as f:
        raw_data = yaml.safe_load(f)

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
