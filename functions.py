import os

from price_parser import WBPriceParser


def getting_search_req(result):
    """формирование url из поискового запроса"""

    search_req = str(input('enter search request: ')).strip()

    result.req = search_req

    # loading_search_req_to_file(search_req)

    search_req = search_req.replace(' ', '%20')
    search_req = f'https://www.wildberries.ru/catalog/0/search.aspx?search={search_req}'

    return search_req


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


def creating_error_log_directory():
    """Создание папки error_log"""

    if not os.path.isdir(f'./error_log'):
        os.mkdir(f'./error_log')
