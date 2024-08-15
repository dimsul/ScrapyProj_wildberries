import multiprocessing
import time
import numpy

from wildberries_crawler import WBCrawler
from price_parser import WBPriceParser
from functions import getting_search_req, run_parser, get_median, get_avg, clear_parsing_result_from_errors


def main():

    time_ = time.time()

    # Формируем url для поиска товаров
    search_url = getting_search_req()

    # Формируем список ссылок на товары
    crawler = WBCrawler(search_url)
    urls_to_products = crawler.run()

    # Формируем список из цен и ссылок на товары
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()-1)
    parsing_result = pool.map(run_parser, urls_to_products)

    print(time.time() - time_)

    print()

    # Удаляем результаты парсинга отработавшего с ошибкой, если такой есть
    parsing_result = clear_parsing_result_from_errors(parsing_result)

    len(parsing_result)

    for i in parsing_result:
        print(i)

    prices = tuple([elem[0] for elem in parsing_result])
    median = get_median(prices)
    avg = get_avg(prices)
    print(median)
    print(avg)


if __name__ == '__main__':

    main()
