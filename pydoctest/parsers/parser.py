from typing import List


class Parameter():
    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type


class Parser():
    def get_parameters(self, doc: str) -> List[Parameter]:
        raise NotImplementedError()

    def get_return_type(self, doc: str) -> str:
        raise NotImplementedError()
