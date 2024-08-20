from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp_con
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class WBPriceScraper:
    """Скрапер поиска цены на товар"""

    url: str = None

    def __post_init__(self):

        self.__driver = webdriver.Edge()

    def run(self):
        """Запуск парсера"""

        try:

            self.__driver.get(self.url)
            self.__wait()
            value_to_return = (self.__get_price(), self.url)    # Возвращаем кортеж из цены и url

        except Exception as err:
            value_to_return = err   # Возвращаем сообщение об ошибке

        finally:
            self.__driver.close()
            self.__driver.quit()

        return value_to_return

    def __wait(self):
        """Запуск ожидания загрузки всей страницы"""

        wait = WebDriverWait(self.__driver, 10)
        wait.until(exp_con.presence_of_element_located((By.XPATH, '//p[@class="price-block__price-wrap "]')))

    def __get_price(self) -> int:
        """Возвращает цену в виде int"""

        res = self.__driver.find_element(By.XPATH, '//p[@class="price-block__price-wrap "]')
        soup = BeautifulSoup(res.get_attribute('innerHTML'), 'html.parser')
        price_str = soup.select('ins')[-1].text

        return self.__price_to_int(price_str)

    @staticmethod
    def __price_to_int(price: str):
        """Преобразует цену в int"""

        chars_to_replace = (' ', '\xa0', '₽')

        for char in chars_to_replace:
            price = price.replace(char, '')

        return int(price)
