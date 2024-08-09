from wildberries_crawler import getting_search_req, WBCrawler


def main():

    url = getting_search_req()
    crawler = WBCrawler(url)

    res = crawler.run()
    print(res)


if __name__ == '__main__':

    main()
