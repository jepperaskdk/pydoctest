DEBUG = False


def set_verbose(value: bool) -> None:
    global DEBUG
    DEBUG = value


def log(message: str) -> None:
    global DEBUG
    if DEBUG:
        print(message)
