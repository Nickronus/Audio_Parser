from characteristic_executor.abstract_characteristic_executor_creator import AbstractCharacteristicExecutorCreator
from characteristic_saver.i_characteristic_saver import ICharacteristicSaver
from characteristic_processor.speech_characteristic_processor import SpeechCharacteristicProcessor
from characteristic_processor.voice_characteristic_processor import VoiceCharacteristicProcessor


class IEEEDatabaseParser():
    def __init__(self, 
                characteristic_executor_creator: AbstractCharacteristicExecutorCreator,
                characteristic_saver: ICharacteristicSaver):
        self.__voice_characteristic_processor = VoiceCharacteristicProcessor(characteristic_executor_creator, characteristic_saver)
        self.__speech_characteristic_processor = SpeechCharacteristicProcessor(characteristic_executor_creator, characteristic_saver)

    def parse(self):
        print('Enter folder path: ')
        folder_path = input()
        print('Enter number of experiment: \n Speech experiment - 1 \n Voice experiment - 2')
        number_of_experiment = input()
        print('Enter output filename: ')
        output_filename = input()

        match number_of_experiment:
            case '1':
                self.__voice_characteristic_processor.process(folder_path, ["^VA", "^VA", "^VE", "^VI", "^VO", "^VU"], output_filename)

            case '2':
                self.__speech_characteristic_processor.process(folder_path, ["^B1", "^B2", "^FB", "^D1", "^D2"], output_filename)