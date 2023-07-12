import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


def extractors_tourtoctoc():
    # Chrome 옵션 설정
    options = Options()
    options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'  # Chrome 실행 파일 경로를 자신의 환경에 맞게 설정해주세요.

    # 웹 드라이버 초기화
    driver = webdriver.Chrome(options=options)  # ChromeOptions를 사용하여 WebDriver 초기화
    driver.implicitly_wait(10)

    # 페이지 범위 설정
    start_page = 1
    end_page = 3
    number = 1
    # end_page =

    # 이미 클릭한 요소를 저장하는 리스트
    results = []

    # 페이지 순회
    for page in range(start_page, end_page + 1):
        try:
            # 페이지 접속
            url = f'https://www.tourtoctoc.com/news/articleList.html?page={page}'
            driver.get(url)
            time.sleep(3)  # 페이지가 로드될 때까지 대기 (필요에 따라 조정)

            # 원하는 요소 찾기
            elements = driver.find_elements(By.CSS_SELECTOR, 'section#section-list ul.types li a')
            print(len(elements))
            # 요소 클릭 및 크롤링
            for i in range(0, len(elements)):
                print("contents number : " + str(number))
                number += 1
                element = elements[i]
                # 이미 클릭한 요소인지 확인
                if element in results:
                    continue

                # Click on the <a> tag inside the element using JavaScript
                driver.execute_script("arguments[0].click();", element)
                time.sleep(1)  # 페이지가 로드될 때까지 대기 (필요에 따라 조정)

                # 페이지 소스코드 가져오기
                page_source = driver.page_source

                # BeautifulSoup으로 파싱
                soup = BeautifulSoup(page_source, 'html.parser')
                print("is it working???????????????")
                # 원하는 데이터 추출
                # 예시로 'restaurant-name' 클래스를 가진 요소의 텍스트를 추출합니다.
                content = soup.select_one('article#article-view-content-div p').get_text(strip=True)
                # document_elements = driver.find_elements(By.CSS_SELECTOR, '.txt')

                document_text = ""

                for element in content:
                    # if not element.find_elements(By.TAG_NAME, 'img'):
                    print("is it working?")
                    text = content.strip()

                    text = re.sub(r'[^0-9a-zA-Z가-힣\s]', '', text)

                    document_text += text + " "

                    data = {
                        'content': document_text
                    }
                    results.append(data)

                # 뒤로 가기
                driver.back()
                time.sleep(1)  # 페이지가 로드될 때까지 대기 (필요에 따라 조정)



        except Exception as e:
            continue

    # 웹 드라이버 종료
    driver.quit()

    return results