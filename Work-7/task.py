from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json

# Установка пользовательского агента
user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')

chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--headless')  # Запуск в фоновом режиме (без GUI)
chrome_options.add_argument('--no-sandbox')  # Для совместимости с некоторыми системами
chrome_options.add_argument('--disable-dev-shm-usage')  # Для систем с ограниченной памятью

# Инициализация веб-драйвера
driver = webdriver.Chrome(options=chrome_options)
url = 'https://author.today/work/tag/бесплатно?ysclid=lz9im1q89l625738659'

try:
    # Открытие сайта
    driver.get(url)
    
    # Подгрузка всех элементов тела
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Прокрутка страницы до конца page_height = driver.execute_script('return document.documentElement.scrollHeight')  # высота страницы
    while True:
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight)')
        time.sleep(2)  # Задержка для подгрузки новых элементов new_height = driver.execute_script('return document.documentElement.scrollHeight')
        if new_height == page_height:  # Если высота не изменилась, значит достигли конца break
        page_height = new_height # XPath для извлечения данных
    titles_xpath = "//div[contains(@class,'book-row-content')]/div[1]/a"
    authors_xpath = "//div[contains(@class,'book-row-content')]/div[2]/a"
    genres_xpath = "//div[contains(@class,'book-row-content')]/div[3]/a[2]"

    # Получение элементов на странице
    titles = driver.find_elements(By.XPATH, titles_xpath)
    authors = driver.find_elements(By.XPATH, authors_xpath)
    genres = driver.find_elements(By.XPATH, genres_xpath)

    # Сбор данных в словарь data = {}
    for i in range(len(titles)):
        title = titles[i].text.strip()  # Удаляем лишние пробелы
        author = authors[i].text.strip()
        genre = genres[i].text.strip()

        data[title] = {'author': author, 'genre': genre}

    # Сохранение данных в JSON файл
    with open('books.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print('Данные сохранены в файл books.json')

except Exception as e:
    print(f'Произошла ошибка: {e}')
finally:
    driver.quit()