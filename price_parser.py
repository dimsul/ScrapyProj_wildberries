from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

import bs4
import dataclasses


@dataclasses.dataclass
class WBPriceParser:

    url: str = None

    def __post_init__(self):

        self.__driver = webdriver.Edge()

    def get_price(self):
        """Запуск парсера"""

        try:
            self.__driver.get(self.url)
            time.sleep(1)
            # self.__scroll_page()
            res = self.__get_price_str()
            print(res, self.url)
        except Exception as err:
            print(err, self.url)
        finally:
            self.__driver.close()
            self.__driver.quit()

    # def __scroll_page(self):
    #     time.sleep(1)
    #     main_page = self.__driver.find_element(By.XPATH, '//html')
    #     # main_page.send_keys(Keys.PAGE_DOWN)
    #     # main_page.send_keys(Keys.PAGE_DOWN)
    #     # main_page.send_keys(Keys.PAGE_DOWN)
    #     # main_page.send_keys(Keys.PAGE_DOWN)
    #     time.sleep(1)

    def __get_price_str(self) -> int:
        """Возвращает цену в виде int"""
        res = self.__driver.find_element(By.XPATH, '//p[@class="price-block__price-wrap "]')
        soup = bs4.BeautifulSoup(res.get_attribute('innerHTML'), 'html.parser')
        price_str = soup.select('ins')[-1].text
        return self.__price_to_int(price_str)

    @staticmethod
    def __price_to_int(price: str):
        """Преобразует цену в int"""
        chars_to_replace = (' ', '\xa0', '₽')
        for char in chars_to_replace:
            price = price.replace(char, '')
        return int(price)


# url = 'https://www.wildberries.ru/catalog/150385348/detail.aspx'
#
# pars = WBPriceParser(url)
# pars.get_price()
