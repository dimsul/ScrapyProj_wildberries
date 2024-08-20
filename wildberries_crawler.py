from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from dataclasses import dataclass


@dataclass
class WBCrawler:
    """Краулер по поиску ссылок на товары"""

    url: str

    def __post_init__(self):

        self.__driver = webdriver.Edge()

    def run(self):
        """Запуск краулера"""

        urls = None

        try:

            self.__driver.get(self.url)
            self.__scroll_all_elem()
            urls = self.__get_links_for_parsing()
            sleep(1)

        except Exception as err:

            with open(f"./error_log/_crawler_err.txt", 'a') as file:
                file.write(f'{err}')

        finally:

            self.__driver.close()
            self.__driver.quit()

        return urls

    def __scroll_all_elem(self):
        """Вывод всех эллементов на страницу
        для последующего поиска ссылок"""

        main_page = self.__driver.find_element(By.XPATH, '//html')

        counter = 20    # Отсечка, если эллементов на странице меньше максимального числа
        while (99 > len(self.__driver.find_elements(by=By.XPATH, value='//div[@class="product-card__wrapper"]'))
               and counter != 0):
            counter -= 1
            main_page.send_keys(Keys.PAGE_DOWN)
            sleep(0.5)

        sleep(1)

    def __get_links_for_parsing(self):
        """Вывод всех ссылок для парсинга цен"""

        value = '//div[@class="product-card-overflow"]//div[@class="product-card__wrapper"]/a'
        attr = 'href'

        return tuple(elem.get_attribute(attr) for elem in self.__driver.find_elements(By.XPATH, value))
