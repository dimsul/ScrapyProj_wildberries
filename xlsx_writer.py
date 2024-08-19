import openpyxl
import dataclasses

from xlsx_reader import OpenXlsxFile


@dataclasses.dataclass
class WriteXlsxFile(OpenXlsxFile):

    row_counter = 2

    value: [int, float]

    def get_list_of_requests(self):
        pass

    def set_data_to_xlsx_file(self):

        self.__insert_data(self.filename, self.value)

    @classmethod
    def __insert_data(cls, filename, value):
        try:
            wb = openpyxl.load_workbook(f'{filename}')
            ws = wb['Расчет']
            ws[f'Z{cls.row_counter}'] = value
            cls.row_counter += 1
            wb.save(f'{filename}')

        except Exception as err:
            with open(f"./error_log/load_to_xlsx_error.txt", 'a') as file:
                file.write(f'{err}')
