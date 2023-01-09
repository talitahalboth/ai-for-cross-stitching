__DEBUG__ = True
__VERBOSE__ = True

def log (message, severity="INFO"):
    """Log a message to the console.

    :param severity: The severity of the message.
    :param message: The message to log.
    """
    if severity == 'DEBUG':
        if __DEBUG__:
            print(f'{severity}: {message}')
    elif severity == "verbose":
        if __VERBOSE__:
            print(f'{severity}: {message}')
    else:
        print(f'{severity}: {message}')
