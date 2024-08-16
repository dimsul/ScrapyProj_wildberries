import multiprocessing
import time
import datetime

from parsing_result import ParsingResult
from wildberries_crawler import WBCrawler
from functions import (getting_search_req, run_parser, creating_error_log_directory)


def main():

    time_ = time.time()

    result = ParsingResult()

    # Создаём папку error_log
    creating_error_log_directory()

    # Формируем url для поиска товаров
    search_url = getting_search_req(result)

    # Формируем список ссылок на товары
    crawler = WBCrawler(search_url)
    urls_to_goods = crawler.run()

    # Формируем список из цен и ссылок на товары
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()-1)
    result.prices_and_urls = pool.map(run_parser, urls_to_goods)

    print(time.time() - time_)

    print()

    result.load_to_file()


if __name__ == '__main__':

    try:
        main()
    except Exception as err:
        with open(f'./{datetime.datetime.now()}__run_error.txt'.replace(':', '_'), 'w') as file:
            file.write('Работа программы завершилась ошибкой:\n\n')
            file.write(f'{err}')
