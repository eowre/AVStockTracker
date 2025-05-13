
#TODO implement loggingHandler
class loggingHandler:
    def __init__(self, logger):
        self.logger = logger

    def log(self, message):
        self.logger.info(message)