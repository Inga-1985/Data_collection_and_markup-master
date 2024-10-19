from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json

user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')

chrome_option = Options()
chrome_option.add_argument(f'user-agent={user_agent}')

# Инициализация веб-драйвера
driver = webdriver.Chrome(options=chrome_option)
url = 'https://author.today/work/tag/бесплатно?ysclid=lz9im1q89l625738659'

try:
    # Открытие сайта
    driver.get(url)
    
    # Подгрузка всех элементов тела
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    page_height = driver.execute_script('return document.documentElement.scrollHeight')  # высота экрана
    while True:
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight)')
        WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.documentElement.scrollHeight') > page_height)
        new_height = driver.execute_script('return document.documentElement.scrollHeight')
        if new_height == page_height:
            break
        page_height = new_height

    titles_xpath = "//div[contains(@class,'book-row-content')]/div[1]/a"
    authors_xpath = "//div[contains(@class,'book-row-content')]/div[2]/a"
    genres_xpath = "//div[contains(@class,'book-row-content')]/div[3]/a[2]"

    titles = driver.find_elements(By.XPATH, titles_xpath)
    authors = driver.find_elements(By.XPATH, authors_xpath)
    genres = driver.find_elements(By.XPATH, genres_xpath)

    # Проверка, что количество элементов совпадает
    if len(titles) == len(authors) == len(genres):
        data = {}
        for i in range(len(titles)):
            title = titles[i].text
            author = authors[i].text
            genre = genres[i].text

            data[title] = {'author': author.strip(), 'genre': genre.strip()}

        with open('books.json', 'w', encoding='UTF-8', newline='') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print('Данные сохранены в файл books.json')
    else:
        print('Количество загруженных элементов не совпадает!')

except Exception as e:
    print(f'Произошла ошибка: {e}')
finally:
    driver.quit()