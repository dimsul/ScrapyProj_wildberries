from wildberries_crawler import getting_search_req, WBCrawler
from price_parser import WBPriceParser

import multiprocessing
import time


def main():

    time_ = time.time()

    search_url = getting_search_req()
    crawler = WBCrawler(search_url)

    urls_to_products = crawler.run()

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()-1)

    result = pool.map(run_parser, urls_to_products)

    print(time.time() - time_)

    print()

    for i in result:
        print(i)


def run_parser(url):
    """Запускает парсер и возвращает результат его работы"""

    return WBPriceParser(url).run()


if __name__ == '__main__':

    main()
