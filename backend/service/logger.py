import json


def _log(level, message):
    """Log a message to the console.

    Args:
        level (str): The level of the message.
        message (str): The message to log.
    """
    if isinstance(message, dict):
        message = json.dumps(message)

    print(json.dumps({"level": level, "message": message}))


def info(message):
    """Log a message to the console.

    Args:
        message (str): The message to log.
    """
    _log("info", message)


def error(message):
    """Log a message to the console.

    Args:
        message (str): The message to log.
    """
    _log("error", message)


def debug(message):
    """Log a message to the console.

    Args:
        message (str): The message to log.
    """
    _log("debug", message)
