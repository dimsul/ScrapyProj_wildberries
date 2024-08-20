from multiprocessing import Pool, cpu_count
from datetime import datetime

from parsing_result import ParsingResult
from wildberries_crawler import WBCrawler
from functions import getting_search_req, run_price_scraper, creating_error_log_directory
from xlsx_reader import XlsxReader


def main(req):

    result = ParsingResult()

    # Создаём папку error_log
    creating_error_log_directory()

    # Формируем url для поиска товаров
    search_url = getting_search_req(result, req)

    # Формируем список ссылок на товары
    crawler = WBCrawler(search_url)
    urls_to_goods = crawler.run()

    # Формируем список из цен и ссылок на товары
    pool = Pool(processes=cpu_count()-1)
    result.prices_and_urls = pool.map(run_price_scraper, urls_to_goods)

    result.load_to_files()


if __name__ == '__main__':

    # Формируем список запросов
    try:

        file = XlsxReader(r'./Юнит ВБ.xlsx')
        requests = file.get_list_of_requests()

    except FileExistsError:
        requests = None

    # Собираем данные
    for request in requests:

        try:
            main(request)
        except Exception as err:
            with open(f'./{datetime.now()}__run_error.txt'.replace(':', '_'), 'w') as file:
                file.write('Работа программы завершилась ошибкой:\n\n')
                file.write(f'{err}')
