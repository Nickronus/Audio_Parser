from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '../')

from i_characteristic_saver import ICharacteristicSaver
from characteristic import Characteristic

class IEEEDatabaseExcelCharacteristicSaver(ICharacteristicSaver):
    def __init__(self, excel_characteristic_saver: ICharacteristicSaver):
        self.__excel_characteristic_saver = excel_characteristic_saver

    def save(self, header_and_data: dict[str, list[str]], output_filename: str):
        is_sick = 'Is sick'
        header_and_data_node = {is_sick: []}
        header_and_data.update(header_and_data_node)
        for i in range(len(header_and_data[Characteristic.FILEPATH.name])):
            filepath = header_and_data[Characteristic.FILEPATH.name][i]
            if "28 People with Parkinson's disease" in filepath:
                header_and_data[is_sick].append('Yes')
            elif "22 Elderly Healthy Control" in filepath:
                header_and_data[is_sick].append('No')
            elif "15 Young Healthy Control" in filepath:
                header_and_data[is_sick].append('No')
            else:
               header_and_data[is_sick].append('-')
            
            header_and_data[Characteristic.FILEPATH.name][i] = filepath.rsplit("/", 1)[-1]
            
        self.__excel_characteristic_saver.save(header_and_data, output_filename)