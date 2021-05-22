from pydoctest.validation import ValidationResult
from pydoctest.configuration import Configuration


class Reporter():
    def __init__(self, config: Configuration) -> None:
        self.config = config

    def get_output(self, result: ValidationResult) -> str:
        raise NotImplementedError()
