from abc import ABC, abstractmethod
from collections.abc import Callable

#: Callable[[str, bytes, Callable[[bytes], None]], None]
# from path_resolve.core import add_relative_path_to_sys
# add_relative_path_to_sys(__file__, '../framework')

from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '../')

from characteristic import Characteristic
from characteristic_extractor.abstract_characteristic_extractor_creator import AbstractCharacteristicExtractorCreator
from characteristic_saver.i_characteristic_saver import ICharacteristicSaver

from characteristic_extractor.i_characteristic_extractor import ICharacteristicExtractor
from file_paths_extractor import FilePathsExtractor
from characteristic_extractor.abstract_characteristic_extractor_creator import AbstractCharacteristicExtractorCreator
from characteristic_saver.i_characteristic_saver import ICharacteristicSaver

class AbstractCharacteristicProcessor(ABC):
    """Абстрактный процессор характеристик аудиофайла.
    """    
    def __init__(self, 
                characteristic_extractor_creator: AbstractCharacteristicExtractorCreator,
                characteristic_saver: ICharacteristicSaver):
        self._characteristic_extractor_creator = characteristic_extractor_creator
        self._characteristic_saver = characteristic_saver

    def process(self, folder_path: str, file_patterns: list[str], output_filename: str):
        """Извлекает пути к файлам (FilePathsExtractor), 
        извлекает характеристики аудиофайлов (ICharacteristicExtractor),
        сохраняет данные (ICharacteristicSaver).

        Args:
            folder_path (str): Путь к папке с файлами.
            file_patterns (list[str]): Паттерн файлов.
            output_filename (str): Имя сохраняемого файла.
        """        
        file_paths_list:list[str] = FilePathsExtractor.extract(folder_path, file_patterns)
        header_and_data: dict[str, list[str]] = {}
        header_and_data_node = {Characteristic.FILEPATH.name: []}
        header_and_data.update(header_and_data_node)
        file_counter = 0
        print('Start processing.')
        for file_path in file_paths_list:
            characteristic_extractor: ICharacteristicExtractor = \
                self._characteristic_extractor_creator.create_characteristic_extractor(file_path)
            methods: list[Callable[[], dict[Characteristic: float]]] = \
                self._create_characteristic_extractor_methods_list(characteristic_extractor)
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
            print(f"Processed files: {file_counter}", end='\r')

        print('\n')

        self._characteristic_saver.save(header_and_data, output_filename)

    @abstractmethod
    def _create_characteristic_extractor_methods_list(self, characteristic_extractor: ICharacteristicExtractor) ->list[Callable[[], dict[Characteristic: float]]]:
        """Создать список вызываемых у ICharacteristicExtractor методов.
        Реализации статически закрепляют список характеристик, которые необходимо получить.
        """
        pass