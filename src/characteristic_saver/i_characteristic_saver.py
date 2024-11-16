from abc import ABC, abstractmethod

from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '../')

from characteristic import Characteristic

class ICharacteristicSaver(ABC):
    """Интерфейс для классов, сохраняющих файлы.
    """    
    @abstractmethod
    def save(header_and_data: dict[str, list[str]], output_filename: str):
        """Сохранить файл.

        Args:
            header_and_data (dict[str, list[str]]): Словарь из заголовков и списка данных для них.
            output_filename (str): Полное имя сохраняемого фала.
        """        
        pass