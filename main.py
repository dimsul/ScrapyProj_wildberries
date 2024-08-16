import multiprocessing
import time
import datetime

from wildberries_crawler import WBCrawler
from functions import (getting_search_req, run_parser, clear_parsing_result_from_errors, load_result_to_file,
                       creating_error_log_directory)


def main():

    time_ = time.time()

    # Создаём папку error_log
    creating_error_log_directory()

    # Формируем url для поиска товаров
    search_url = getting_search_req()

    # Формируем список ссылок на товары
    crawler = WBCrawler(search_url)
    urls_to_goods = crawler.run()

    # Формируем список из цен и ссылок на товары
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()-1)
    parsing_result = pool.map(run_parser, urls_to_goods)

    print(time.time() - time_)

    print()

    # Удаляем результаты парсинга отработавшего с ошибкой, если такой есть
    parsing_result = clear_parsing_result_from_errors(parsing_result)

    # Загружаем результаты работы в файл
    load_result_to_file(parsing_result, tuple([elem[0] for elem in parsing_result]))


if __name__ == '__main__':

    try:
        main()
    except Exception as err:
        with open(f'./{datetime.datetime.now()}__run_error.txt'.replace(':', '_'), 'w') as file:
            file.write('Работа программы завершилась ошибкой:\n\n')
            file.write(f'{err}')
