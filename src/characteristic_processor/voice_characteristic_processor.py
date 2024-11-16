from collections.abc import Callable

from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '../')

from characteristic import Characteristic
from characteristic_executor.i_characteristic_executor import ICharacteristicExecutor
from file_paths_executor import FilePathsExecutor
from abstract_characteristic_processor import AbstractCharacteristicProcessor
from characteristic_executor.abstract_characteristic_executor_creator import AbstractCharacteristicExecutorCreator
from characteristic_saver.i_characteristic_saver import ICharacteristicSaver

class VoiceCharacteristicProcessor(AbstractCharacteristicProcessor):
    def __init__(self, 
                characteristic_executor_creator: AbstractCharacteristicExecutorCreator,
                characteristic_saver: ICharacteristicSaver):
        AbstractCharacteristicProcessor.__init__(self, characteristic_executor_creator, characteristic_saver)

    def _create_characteristic_executor_methods_list(self, characteristic_executor: ICharacteristicExecutor) ->list[Callable[[], dict[Characteristic: float]]]:
        return [characteristic_executor.get_jitter_ppq5,
                characteristic_executor.get_shimmer_local,
            #    characteristic_executor.get_nhr,
                characteristic_executor.get_hnr]