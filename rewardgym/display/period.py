class BasePeriod:
    def __init__(self, name, onset, duration, **kwargs):
        self.name = name
        self.onset = onset
        self.duration = duration
        self.started = False
        self.ended = False
        self.kwargs = kwargs

    def start(self, t, logger):
        if not self.started and t >= self.onset:
            logger.log_event({"event_type": self.kwargs.get("log_on_onset", self.name)})
            self.started = True

    def end(self, t, logger):
        if self.started and t >= self.onset + self.duration:
            logger.log_event(
                {"event_type": self.kwargs.get("log_on_offset", f"{self.name}_end")}
            )
            self.ended = True

    def update(self, t, logger, win):
        self.start(t, logger)
        self.handle(t, logger, win)
        self.end(t, logger)

    def handle(self, t, logger, win):
        # To be implemented in subclasses
        pass


class ResponsePeriod(BasePeriod):
    pass
