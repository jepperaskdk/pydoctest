from typing import List, Type
from types import ModuleType


class Parameter():
    def __init__(self, name: str, t: Type) -> None:
        self.name = name
        self.type = t


class Parser():
    def get_parameters(self, doc: str, module_type: ModuleType) -> List[Parameter]:
        raise NotImplementedError()

    def get_return_type(self, doc: str, module_type: ModuleType) -> Type:
        raise NotImplementedError()
