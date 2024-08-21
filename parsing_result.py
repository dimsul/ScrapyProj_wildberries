from dataclasses import dataclass
from numpy import median, average
from xlsx_writer import XlsxWriter

from params import XLSX_FILENAME


@dataclass
class ParsingResult:
    """Результат работы парсера"""

    req: str = None
    prices_and_urls: [list, tuple, set] = None

    def load_to_files(self):
        """Запись результатов в файл"""

        # Удаляем результаты парсинга отработавшего с ошибкой, если такой есть
        self.__clear_parsing_result_from_errors()

        with open('./parsing_result.txt', 'a') as file:

            # Записываем поисковый запрос
            file.write(f'{"|" * 120}\n\n')
            file.write(f'Поисковый запрос: {self.req}\n\n')

            # Записываем результаты парсинга
            for price_and_url in self.prices_and_urls:
                file.write(f'Стоимость товара: {price_and_url[0]}, ссылка на товар - {price_and_url[1]}\n')

            # Вычисляем медианное и среднее значения
            median_ = median([elem[0] for elem in self.prices_and_urls])
            average_ = average([elem[0] for elem in self.prices_and_urls])

            # Записываем медианное и среднее значения
            file.write(f'\nМедианное значение цены: {median_}\n')
            file.write(f'\nСреднее значение цены: {average_}\n')

            file.write(f'\n{"|" * 120}\n')

        # Так-же записываес среднее значение в xlsx-файл
        XlsxWriter(XLSX_FILENAME, average_).set_data_to_xlsx_file()

    def __clear_parsing_result_from_errors(self):
        """Удаление ошибочных результатов работы пврсера"""

        self.prices_and_urls = set(self.prices_and_urls)

        if None in self.prices_and_urls:
            self.prices_and_urls.remove(None)

        if len(self.prices_and_urls) == 0:

            XlsxWriter(XLSX_FILENAME, 'ERROR').set_data_to_xlsx_file()
            raise ValueError(f'Не найдено ни одного результата (либо запрос сформирован некорректно,\n'
                             f'либо произошел сбой при поиске цены)')
