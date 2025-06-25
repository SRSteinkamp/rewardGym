# get_env.py
import importlib
import os

TASKS_PATH = "tasks"


def _discover_plugins():
    task_map = {}
    for task_folder in os.listdir(TASKS_PATH):
        plugin_path = f"{TASKS_PATH}.{task_folder}.plugin"
        try:
            plugin_module = importlib.import_module(plugin_path)
            registry = plugin_module.register()
            task_map.update(registry)  # e.g., {"task_a": get_task}
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"[WARN] Could not register task '{task_folder}': {e}")
    return task_map


# Cache the registry to avoid reloading on every call
TASK_REGISTRY = _discover_plugins()


def get_env(task_name: str, mode="experiment", config=None):
    if task_name not in TASK_REGISTRY:
        raise ValueError(f"Unknown task: {task_name}")
    task_entry_fn = TASK_REGISTRY[task_name]
    return task_entry_fn(mode=mode, config=config)
