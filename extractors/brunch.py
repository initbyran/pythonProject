import requests
from selenium import webdriver
from selenium.webdriver import Keys
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.by import By

def extractors_brunch(keyword):
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('headless')
    driver = webdriver.Chrome(options=webdriver_options)
    driver.maximize_window()
    driver.implicitly_wait(2)

    base_url = 'https://brunch.co.kr/'
    driver.get(url = f'{base_url}search?q={keyword}')
    response = requests.get(f'{base_url}{keyword}')
    soup = BeautifulSoup(response.text, 'html.parser')

    SCROLL_PAUSE_TIME = 4

    last_height = driver.execute_script("return document.body.scrollHeight")
    cnt = 0
    cooking = []
    start_page = 0

    while cnt < 3:
        cnt += 1
        print(cnt)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        print('????')
        print("brunch-{} ~ {}".format(start_page, start_page+19))
        for page in range(start_page, start_page+19):
            try:
                acting_point = driver.find_element(By.XPATH,
                    f'//*[@id="resultArticle"]/div/div[1]/div[2]/ul/li[{page}]/a/div[1]/strong')
                driver.execute_script("arguments[0].click();", acting_point)
                time.sleep(SCROLL_PAUSE_TIME)
            except:
                pass

            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                driver.get_window_position(driver.window_handles[1])
                driver.implicitly_wait(2)
            else:
                print("No new window opened")
                continue  # skip this loop if no new window is opened

            driver.switch_to.window(driver.window_handles[1])
            driver.get_window_position(driver.window_handles[1])
            driver.implicitly_wait(2)

            for entry in soup.select('.wrap_article_list > ul > li'):
                link = 'https://brunch.co.kr' + entry.select_one('a')['href']

                entry_response = requests.get(link)
                print(link)
                entry_soup = BeautifulSoup(entry_response.text, 'html.parser')
                title = entry_soup.select_one('h1#cover_title').text.strip() if entry_soup.select_one('h1#cover_title') is not None else "Unknown"
                content = entry_soup.select_one('p#wrap_item item_type_text').text.strip() if entry_soup.select_one('p#wrap_item item_type_text') is not None else "Unknown"

            time.sleep(SCROLL_PAUSE_TIME)

            cooking.append({
                "title": title,
                "content": content
            })
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.get_window_position(driver.window_handles[0])
            print(title)
        start_page += 19

    return cooking




    # if cnt % 10 == 0:
    #     f = open("cooking.csv", "a", encoding="UTF-8", newline='')
    #     csvWriter = csv.writer(f)
    #     for i in cooking:
    #         csvWriter.writerow([i["title"], i["date"], i["content"], i['img']])
    #     f.close()
