import openpyxl
import dataclasses
import os


@dataclasses.dataclass
class OpenXlsxFile:

    filename: str

    def __post_init__(self):

        if not os.path.isfile(self.filename):
            raise FileNotFoundError

    def get_list_of_requests(self):

        try:
            ws = openpyxl.load_workbook(f'{self.filename}')
            requests = []
            row = 2
            while True:
                if ws['Расчет'].cell(row, 25).value is None:
                    break
                else:
                    requests.append(ws['Расчет'].cell(row, 25).value)
                    row += 1
        except Exception:
            raise FileExistsError

        return requests
