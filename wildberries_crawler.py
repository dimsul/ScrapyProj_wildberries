from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import dataclasses


def getting_search_req():
    """формирование url из поискового запроса"""

    search_req = str(input('enter search request: '))
    search_req = search_req.replace(' ', '%20')
    search_req = f'https://www.wildberries.ru/catalog/0/search.aspx?search={search_req}'

    return search_req


@dataclasses.dataclass
class WBCrawler:

    url: str

    def __post_init__(self):

        self.__driver = webdriver.Edge()

    def run(self):

        urls = None

        try:
            self.__driver.get(self.url)
            self.__out_all_elem()
            urls = self.__get_links_for_parsing()
            time.sleep(1)
        except Exception as err:
            print(err)
        finally:
            self.__driver.close()
            self.__driver.quit()

        return urls

    def __out_all_elem(self):
        """Вывод всех эллементов на страницу
        для последующего поиска ссылок"""

        main_page = self.__driver.find_element(By.XPATH, '//html')

        while 99 > len(self.__driver.find_elements(by=By.XPATH, value='//div[@class="product-card__wrapper"]')):
            main_page.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)

        time.sleep(1)

    def __get_links_for_parsing(self):
        """Вывод всех ссылок для парсинга цен"""

        value = '//div[@class="product-card__wrapper"]/a'
        attr = 'href'

        return tuple(elem.get_attribute(attr) for elem in self.__driver.find_elements(By.XPATH, value))



# driver = webdriver.Edge()
#
# try:
#     driver.get(getting_search_req())
#
#     out_all_elem(driver)
#
#     links = get_links_for_parsing(driver)
#
#     print(links)
#     time.sleep(30)
# except Exception as err:
#     print(err)
# finally:
#     driver.close()
#     driver.quit()


# print(getting_search_req())
