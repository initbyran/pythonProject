from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwwr_jobs

keyword = input("What do you wnat to search for?")

indeed = extract_indeed_jobs(keyword)
wwr = extract_wwwr_jobs(keyword)

jobs = indeed + wwr
for job in jobs:
    print(job)
    print("/////\n//////")


""" 범수 코드

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException


# URL로 이동합니다.
driver.get('http://info.childcare.go.kr/info/cera/search/findNurseryGrade.jsp')

# 시/도 선택
select_sido = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@id='sidoCode']")))
select_sido.send_keys("서울특별시")

# 시/군/구 선택
sigungu_list = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구",
                "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"]
for sigungu in sigungu_list:
    print(sigungu)
    select_sigungu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sigunguCode")))
    select_sigungu.send_keys(sigungu)
    # 딜레이 추가
    # time.sleep(5)

    # 검색 버튼 클릭
    search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[@alt='검색']")))
    driver.execute_script("arguments[0].click();", search_button)

    while True:
        try:
            # 테이블의 모든 내용을 긁어옵니다.
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#pageLoadResult .tab_content .table_childcare tbody")))
            rows = table.find_elements(By.XPATH, ".//tr[position()>=1]")
            for row in rows:
                cells = row.find_elements(By.XPATH, ".//td")
                for cell in cells:
                    print(cell.text, end='\t')
                print()
            # 다음 페이지로 이동합니다.
            next_page_button = driver.find_element(By.CSS_SELECTOR, ".paging.btn a.next1")
            driver.execute_script("arguments[0].click();", next_page_button)
            # 페이지 로딩을 기다립니다.
            WebDriverWait(driver, 10).until(EC.staleness_of(table))
        except StaleElementReferenceException:
            continue
        except:
            # 마지막 페이지이면 루프를 종료합니다.
            break

# webdriver를 종료합니다.
driver.quit()
"""