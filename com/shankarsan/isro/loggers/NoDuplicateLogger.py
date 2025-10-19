class NoDuplicateLogger:
    def __init__(self, logger):
        self.logger = logger
        self.last_message = None

    def info(self, message):
        if message != self.last_message:
            self.logger.info(message)
            self.last_message = message