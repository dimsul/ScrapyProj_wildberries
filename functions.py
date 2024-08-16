import numpy
import os

from price_parser import WBPriceParser


def getting_search_req():
    """формирование url из поискового запроса"""

    search_req = str(input('enter search request: ')).strip()

    loading_search_req_to_file(search_req)

    search_req = search_req.replace(' ', '%20')
    search_req = f'https://www.wildberries.ru/catalog/0/search.aspx?search={search_req}'

    return search_req


def loading_search_req_to_file(search_req):
    """запись запроса в файл"""

    with open('./parsing_result.txt', 'a') as file:

        file.write(f'{"|"*120}\n\n')
        file.write(f'Поисковый запрос: {search_req}\n\n')


def run_parser(url: str):
    """Запускает парсер и возвращает результат его работы"""

    parser_ = WBPriceParser(url)

    try:

        res = parser_.run()
        if not isinstance(res, tuple):
            res = run_parser(url)

    except Exception as err:

        res = None
        run_parser_error_log(url, err)

    return res


def run_parser_error_log(url, err):
    """создание файла ошибки при работе парсера"""

    with open(f"./error_log/{url.split('/')[-2]}.txt", 'w') as file:
        file.write(f'URL: {url}\n\n')
        file.write(f'{err}')


def get_median(prices):
    """получение медианного значения цены"""

    return numpy.median(prices)


def get_avg(prices):
    """получение среднего значения цены"""

    return numpy.average(prices)


def clear_parsing_result_from_errors(parsing_result: list) -> tuple:
    """Удаление ошибочных результатов работы пврсера"""

    parsing_result = set(parsing_result)

    if None in parsing_result:
        parsing_result.remove(None)

    if len(parsing_result) == 0:
        raise ValueError(f'Не найдено ни одного результата (либо запрос сформирован некорректно,\n'
                         f'либо произошел сбой при поиске цены)')

    return tuple(parsing_result)


def load_result_to_file(parsing_result, prices):
    """загрузка результатов работы парсера в файл"""

    with open('./parsing_result.txt', 'a') as file:

        for i in parsing_result:
            file.write(f'Стоимость товара: {i[0]}, ссылка на товар - {i[1]}\n')

        file.write(f'\nМедианное значение цены: {get_median(prices)}\n')
        file.write(f'\nСреднее значение цены: {get_avg(prices)}\n')

        file.write(f'\n{"|" * 40}\n')


def creating_error_log_directory():
    """Создание папки error_log"""

    if not os.path.isdir(f'./error_log'):
        os.mkdir(f'./error_log')
