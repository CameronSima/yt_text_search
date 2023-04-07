
def log(message, level='info'):
    """Log a message to the console.

    Args:
        message (str): The message to log.
        level (str): The level of the message. Defaults to 'info'.
    """
    if level == 'info':
        print(message)
    elif level == 'warning':
        print('WARNING: ' + message)
    elif level == 'error':
        print('ERROR: ' + message)
    else:
        print('ERROR: Unknown log level: ' + level)
