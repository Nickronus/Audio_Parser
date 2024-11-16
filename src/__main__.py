from ieee_database_parser import IEEEDatabaseParser
from characteristic_executor.praat_characteristic_executor_creator import PraatCharacteristicExecutorCreator
from characteristic_executor.abstract_characteristic_executor_creator import AbstractCharacteristicExecutorCreator
from characteristic_saver.i_characteristic_saver import ICharacteristicSaver
from characteristic_saver.excel_characteristic_saver import ExcelCharacteristicSaver
from characteristic_saver.ieee_database_excel_characteristic_saver import IEEEDatabaseExcelCharacteristicSaver

if __name__ == '__main__':
    characteristic_executor_creator: AbstractCharacteristicExecutorCreator = PraatCharacteristicExecutorCreator()
    characteristic_saver: ICharacteristicSaver = ExcelCharacteristicSaver()
    ieee_characteristic_saver: ICharacteristicSaver = IEEEDatabaseExcelCharacteristicSaver(characteristic_saver)
    ieee_database_parser = IEEEDatabaseParser(characteristic_executor_creator, ieee_characteristic_saver)
    ieee_database_parser.parse()
    print('Parsed successful.')