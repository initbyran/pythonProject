import requests
from selenium import webdriver
from selenium.webdriver import Keys
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.by import By
def extractors_naverblog_travel1():
    # 크롬드라이버 실행
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('headless')
    driver = webdriver.Chrome(options=webdriver_options)
    driver.maximize_window()
    driver.implicitly_wait(2)
    results = []
    base_url = 'https://post.naver.com/my/series/detail.naver?memberNo=30482008&seriesNo=285661'
    driver.get(url=base_url)
    # 더보기 계속 클릭하기
    while True:
        try:
            btn_more = driver.find_element_by_css_selector('#more_btn')
            btn_more.click()
            # time.sleep(1)
        except:
            break

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for entry in soup.select('#el_list_container > ul > ul > li'):
        link = 'https://post.naver.com/' + entry.select_one('a')['href']
        entry_response = requests.get(link)
        entry_soup = BeautifulSoup(entry_response.text, 'html.parser')

        title = entry_soup.find("h3", class_="se_textarea")
        content = entry_soup.find("div", class_="se_component_wrap sect_dsc __se_component_area").text.strip() if entry_soup.find("div", class_="se_component_wrap sect_dsc __se_component_area") is not None else "Unknown"

        title = title.replace('\n', '')
        title = title.replace('\t', '')
        title = title.replace('  ', '')
        content = content.replace('\n', '')
        content = content.replace('\t', '')
        content = content.replace('  ', '')

        data = {
            'title': title,
            'content': content
        }
        results.append(data)
        print(title)

    return results