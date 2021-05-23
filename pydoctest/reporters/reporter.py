from pydoctest.validation import ValidationResult
from pydoctest.configuration import Configuration


class Reporter():
    def __init__(self, config: Configuration) -> None:
        """Creates a new Reporter, which uses the config provided.

        Args:
            config (Configuration): Config which specifies rules about reporting.
        """
        self.config = config

    def get_output(self, result: ValidationResult) -> str:
        """Base function for returning output by walking the ValidationResult object.

        Args:
            result (ValidationResult): The results from running Pydoctest.

        Raises:
            NotImplementedError: Raised if this is not implemented by subclasses.

        Returns:
            str: The output to be returned.
        """
        raise NotImplementedError()
