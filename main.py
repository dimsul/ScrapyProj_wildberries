from wildberries_crawler import getting_search_req, WBCrawler
from price_parser import WBPriceParser


def main():

    url = getting_search_req()
    crawler = WBCrawler(url)

    res = crawler.run()
    for i in res:
        WBPriceParser(i).run()


if __name__ == '__main__':

    main()
