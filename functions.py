from os import path, mkdir

from price_scraper import WBPriceScraper


def getting_search_req(result, request: (str, None) = None):
    """формирование url из поискового запроса"""

    if request is None:
        search_req = str(input('enter search request: ')).strip()

    else:
        search_req = request.strip()

    # Сохраняем запрос в результатах для записи в файл
    result.req = search_req

    # Формируем url с запросом
    search_req = search_req.replace(' ', '%20')
    search_req = f'https://www.wildberries.ru/catalog/0/search.aspx?search={search_req}'

    return search_req


def run_price_scraper(url: str):
    """Запускает парсер и возвращает результат его работы"""

    try:

        res = WBPriceScraper(url).run()
        if not isinstance(res, tuple):
            res = run_price_scraper(url)

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

    if not path.isdir(f'./error_log'):
        mkdir(f'./error_log')
