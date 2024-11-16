from abc import ABC, abstractmethod

from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '.')
from i_characteristic_executor import ICharacteristicExecutor

class AbstractCharacteristicExecutorCreator(ABC):
    @abstractmethod
    def create_characteristic_executor(self, file_path: str) -> ICharacteristicExecutor:
        pass