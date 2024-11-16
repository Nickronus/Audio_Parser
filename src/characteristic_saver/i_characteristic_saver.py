from abc import ABC, abstractmethod

from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '../')

from characteristic import Characteristic

class ICharacteristicSaver(ABC):
    @abstractmethod
    def save(header_and_data: dict[str, list[str]], output_filename: str):
        pass