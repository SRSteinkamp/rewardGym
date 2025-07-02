class BaseHook:
    def __init__(self, hook_type="before_trial", **kwargs):
        self.hook_type = hook_type
        self.kwargs = kwargs

    def execute(self, env, stimuli, state: dict):
        """
        env: your runtime environment (timing, win, etc.)
        stimuli: list of stimulus dicts (can be modified in place)
        state: mutable dict for any temporary trial state
        """
        raise NotImplementedError


class RewardHook(BaseHook):
    def execute(self, *args, **kwargs):
        pass
