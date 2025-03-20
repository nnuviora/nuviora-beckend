import logging


loggerObj = logging.getLogger(__name__)
loggerObj.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
loggerObj.addHandler(consoleHandler)


def get_logger():
    return loggerObj
