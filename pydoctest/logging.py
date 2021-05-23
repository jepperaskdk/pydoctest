DEBUG = False


def set_verbose(value: bool) -> None:
    """Change the DEBUG value to be verbose or not.

    Args:
        value (bool): Verbosity on or off.
    """
    global DEBUG
    DEBUG = value


def log(message: str) -> None:
    """Logs the message to stdout if DEBUG is enabled.

    Args:
        message (str): Message to be logged.
    """
    global DEBUG
    if DEBUG:
        print(message)
