from abstract_characteristic_executor_creator import AbstractCharacteristicExecutorCreator

from i_characteristic_executor import ICharacteristicExecutor
from praat_characteristic_executor import PraatCharacteristicExecutor

class PraatCharacteristicExecutorCreator(AbstractCharacteristicExecutorCreator):
    def create_characteristic_executor(self, file_path: str) -> ICharacteristicExecutor:
        return PraatCharacteristicExecutor(file_path)

