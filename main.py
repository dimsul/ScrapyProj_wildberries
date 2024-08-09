from wildberries_crawler import getting_search_req, WBCrawler
from price_parser import WBPriceParser


def main():

    url = getting_search_req()
    crawler = WBCrawler(url)
    # parser = WBPriceParser

    res = crawler.run()
    for i in res:
        print(i)
        # print(WBPriceParser(i).get_price())
    # print(res)


if __name__ == '__main__':

    main()
