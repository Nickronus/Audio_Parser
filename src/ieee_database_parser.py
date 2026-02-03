from characteristic_extractor.abstract_characteristic_extractor_creator import AbstractCharacteristicExtractorCreator
from characteristic_saver.i_characteristic_saver import ICharacteristicSaver
from characteristic_processor.speech_characteristic_processor import SpeechCharacteristicProcessor
from characteristic_processor.voice_characteristic_processor import VoiceCharacteristicProcessor
from characteristic_processor.all_characteristic_processor import AllCharacteristicProcessor
from file_paths_extractor import FilePathsExtractor


class IEEEDatabaseParser():
    """Анализатор базы данных IEEE "Italian Parkinson's Voice and speech".
    """    
    def __init__(self, 
                characteristic_extractor_creator: AbstractCharacteristicExtractorCreator,
                characteristic_saver: ICharacteristicSaver):     
        self.__voice_characteristic_processor = VoiceCharacteristicProcessor(characteristic_extractor_creator, characteristic_saver)
        self.__speech_characteristic_processor = SpeechCharacteristicProcessor(characteristic_extractor_creator, characteristic_saver)
        self.__all_characteristic_processor = AllCharacteristicProcessor(characteristic_extractor_creator, characteristic_saver)

    def parse(self):
        """Для файлов из введённой папки с базой данных "Italian Parkinson's Voice and speech" будет проведён анализ.
        """        
        print("Enter Italian Parkinson's Voice and speech folder path: ")
        folder_path = input()
        print('Enter number of experiment: \n Voice experiment - 1 \n Speech experiment - 2 \n Voice experiment with all characteristics - 3')
        number_of_experiment = input()
        print('Enter output filename: ')
        output_filename = input()
        match number_of_experiment:
            case '1':
                file_paths_list:list[str] = FilePathsExtractor.extract(folder_path, ["^VA", "^VA", "^VE", "^VI", "^VO", "^VU"])
                self.__voice_characteristic_processor.process(file_paths_list, output_filename)

            case '2':
                file_paths_list:list[str] = FilePathsExtractor.extract(folder_path, ["^B1", "^B2", "^FB", "^D1", "^D2"])
                self.__speech_characteristic_processor.process(file_paths_list, output_filename)

            case '3':
                file_paths_list:list[str] = FilePathsExtractor.extract(folder_path, ["^VA", "^VA", "^VE", "^VI", "^VO", "^VU"])
                self.__all_characteristic_processor.process(file_paths_list, output_filename)