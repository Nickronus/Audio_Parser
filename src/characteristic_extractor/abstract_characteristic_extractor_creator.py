from abc import ABC, abstractmethod

from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '.')
from i_characteristic_extractor import ICharacteristicExtractor

class AbstractCharacteristicExtractorCreator(ABC):
    """Абстрактная Фабрика для создания извлекателей характеристик.
    """    
    @abstractmethod
    def create_characteristic_extractor(self, file_path: str) -> ICharacteristicExtractor:
        """Создать извлекателя характеристик аудиофайла.

        Args:
            file_path (str): Путь к аудиофайлу.

        Returns:
            ICharacteristicExtractor: Интерфейс для извлекателя характеристик.
        """        
        pass