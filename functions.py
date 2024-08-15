import numpy

from price_parser import WBPriceParser


def getting_search_req():
    """формирование url из поискового запроса"""

    search_req = str(input('enter search request: '))
    search_req = search_req.replace(' ', '%20')
    search_req = f'https://www.wildberries.ru/catalog/0/search.aspx?search={search_req}'

    return search_req


def run_parser(url):
    """Запускает парсер и возвращает результат его работы"""

    parser_ = WBPriceParser(url)
    try:
        res = parser_.run()
        if not isinstance(res, tuple):
            res = run_parser(url)
    except RecursionError:
        res = None
    return res


def get_median(prices):
    return numpy.median(prices)


def get_avg(prices):
    return numpy.average(prices)


def clear_parsing_result_from_errors(parsing_result: list) -> tuple:
    parsing_result = set(parsing_result)
    if None in parsing_result:
        parsing_result.remove(None)

    return tuple(parsing_result)
