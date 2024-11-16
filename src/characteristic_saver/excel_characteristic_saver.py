import pandas as pd
import os
import openpyxl

from path_resolve.core import add_relative_path_to_sys
add_relative_path_to_sys(__file__, '../')

from i_characteristic_saver import ICharacteristicSaver

class ExcelCharacteristicSaver(ICharacteristicSaver):
    def save(self, header_and_data: dict[str, list[str]], output_filename: str):
        df = pd.DataFrame(header_and_data)

        if not os.path.exists(output_filename):
            # Новый файл
            df.to_excel(output_filename, index=False)
        else:
            # Добавление в существующий файл

            try:
                # Пытаемся получить данные о количестве строк
                workbook = openpyxl.load_workbook(output_filename)
                sheet = workbook.active # Используем активный лист
                last_row = sheet.max_row
                workbook.close() # Закрываем, чтобы pandas мог работать с файлом

                with pd.ExcelWriter(output_filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, sheet_name=sheet.title, index=False, header=False, startrow=last_row + 1)

            except Exception as e:
                print(f"Ошибка при добавлении данных в существующий файл: {e}")
                # В случае ошибки (например, неверный формат файла) создадим новый файл.
                df.to_excel(output_filename, index=False)