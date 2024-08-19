import dataclasses
import openpyxl

import numpy
from xlsx_writer import WriteXlsxFile


@dataclasses.dataclass
class ParsingResult:

    req: str = None
    prices_and_urls: [list, tuple, set] = None

    def load_to_files(self):

        # Удаляем результаты парсинга отработавшего с ошибкой, если такой есть
        self.__clear_parsing_result_from_errors()

        with open('./parsing_result.txt', 'a') as file:

            # Записываем поисковый запрос
            file.write(f'{"|" * 120}\n\n')
            file.write(f'Поисковый запрос: {self.req}\n\n')

            # Записываем результаты парсинга
            for price_and_url in self.prices_and_urls:
                file.write(f'Стоимость товара: {price_and_url[0]}, ссылка на товар - {price_and_url[1]}\n')

            # Записываем медианное и среднее значения
            file.write(f'\nМедианное значение цены: {numpy.median([elem[0] for elem in self.prices_and_urls])}\n')
            file.write(f'\nСреднее значение цены: {numpy.average([elem[0] for elem in self.prices_and_urls])}\n')

            file.write(f'\n{"|" * 120}\n')

        # Так-же записываес среднее значение в xlsx-файл
        WriteXlsxFile(r'./Юнит ВБ.xlsx', numpy.average([elem[0] for elem in self.prices_and_urls])).set_data_to_xlsx_file()

    def __clear_parsing_result_from_errors(self):
        """Удаление ошибочных результатов работы пврсера"""

        parsing_result = set(self.prices_and_urls)

        if None in parsing_result:
            parsing_result.remove(None)

        if len(parsing_result) == 0:
            raise ValueError(f'Не найдено ни одного результата (либо запрос сформирован некорректно,\n'
                             f'либо произошел сбой при поиске цены)')

        # return tuple(parsing_result)
