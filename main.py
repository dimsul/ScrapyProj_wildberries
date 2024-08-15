from wildberries_crawler import getting_search_req, WBCrawler
from price_parser import WBPriceParser

import multiprocessing
import time
import psutil


def main():

    time_ = time.time()

    url = getting_search_req()
    crawler = WBCrawler(url)

    res = crawler.run()
    # for i in res:
    #     WBPriceParser(i).run()

    pool = multiprocessing.Pool(processes=psutil.cpu_count(logical=False)-1)

    result = pool.map(run_parser, res)

    # processess = {}
    # for url in res:
    #     processess[url] = multiprocessing.Process(target=run_parser, args=(url,), daemon=True)
    #
    # for url in processess:
    #     processess[url].start()
    #
    # for url in processess:
    #     processess[url].join()

    print(time.time() - time_)

    print()

    for i in result:
        print(i)


def run_parser(url):
    parser_ = WBPriceParser(url)
    res = parser_.run()
    if not isinstance(res, tuple):
        res = run_parser(url)
    return res


if __name__ == '__main__':

    main()
