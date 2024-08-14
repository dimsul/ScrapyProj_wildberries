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

    def run(self, sleep=1):
        """Запуск парсера"""

        try:
            self.__driver.get(self.url)
            time.sleep(sleep)
            res = self.__get_price()
            print(res, self.url)
        except Exception as err:
            # print(err, self.url)
            if 'no such element' in err:
                self.run(sleep=sleep+1)
            else:
                print(err)
        finally:
            self.__driver.close()
            self.__driver.quit()

    def __get_price(self) -> int:
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
