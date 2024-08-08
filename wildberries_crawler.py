from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def getting_search_req():
    """формирование url из поискового запроса"""
    search_req = str(input('enter search request: '))
    search_req = search_req.replace(' ', '%20')
    search_req = f'https://www.wildberries.ru/catalog/0/search.aspx?search={search_req}'
    return search_req


driver = webdriver.Edge()

try:
    driver.get(getting_search_req())
    main_page = driver.find_element(By.XPATH, '//html')

    while 99 > len(driver.find_elements(by=By.XPATH, value='//div[@class="product-card__wrapper"]')):
        main_page.send_keys(Keys.PAGE_DOWN)

    time.sleep(1)
    links = []
    for element in driver.find_elements(By.XPATH, '//div[@class="product-card__wrapper"]/a'):
        links.append(element.get_attribute('href'))

    print(links)
    time.sleep(30)
except Exception as err:
    print(err)
finally:
    driver.close()
    driver.quit()


# print(getting_search_req())
