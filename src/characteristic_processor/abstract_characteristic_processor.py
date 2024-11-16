from abc import ABC, abstractmethod
from collections.abc import Callable

#: Callable[[str, bytes, Callable[[bytes], None]], None]
# from path_resolve.core import add_relative_path_to_sys
# add_relative_path_to_sys(__file__, '../framework')

from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '../')

from characteristic import Characteristic
from characteristic_executor.abstract_characteristic_executor_creator import AbstractCharacteristicExecutorCreator
from characteristic_saver.i_characteristic_saver import ICharacteristicSaver

from characteristic_executor.i_characteristic_executor import ICharacteristicExecutor
from file_paths_executor import FilePathsExecutor
from characteristic_executor.abstract_characteristic_executor_creator import AbstractCharacteristicExecutorCreator
from characteristic_saver.i_characteristic_saver import ICharacteristicSaver

class AbstractCharacteristicProcessor(ABC):
    def __init__(self, 
                characteristic_executor_creator: AbstractCharacteristicExecutorCreator,
                characteristic_saver: ICharacteristicSaver):
        self._characteristic_executor_creator = characteristic_executor_creator
        self._characteristic_saver = characteristic_saver

    def process(self, folder_path: str, file_patterns: list[str], output_filename: str):
        file_paths_list:list[str] = FilePathsExecutor.execute(folder_path, file_patterns)
        header_and_data: dict[str, list[str]] = {}
        header_and_data_node = {Characteristic.FILEPATH.name: []}
        header_and_data.update(header_and_data_node)
        file_counter = 0
        for file_path in file_paths_list:
            characteristic_executor: ICharacteristicExecutor = \
                self._characteristic_executor_creator.create_characteristic_executor(file_path)
            methods: list[Callable[[], dict[Characteristic: float]]] = \
                self._create_characteristic_executor_methods_list(characteristic_executor)
            characteristics_dict: dict[Characteristic: float] = {}

            for method in methods:
                characteristics_dict.update(method())

            header_and_data[Characteristic.FILEPATH.name].append(file_path)
            for key, value in characteristics_dict.items():
                if not key.name in header_and_data:
                        header_and_data_node = {key.name: []}
                        header_and_data.update(header_and_data_node)

                header_and_data[key.name].append(value)

            file_counter += 1
            if (file_counter % 10) == 0:
                 print(f"Processed files: {file_counter}")

        self._characteristic_saver.save(header_and_data, output_filename)

    @abstractmethod
    def _create_characteristic_executor_methods_list(self, characteristic_executor: ICharacteristicExecutor) ->list[Callable[[], dict[Characteristic: float]]]:
        pass