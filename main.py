from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from requests import get

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)

def get_page_count(keyword):
    base_url = "https://kr.indeed.com/jobs?"
    browser.get(f"{base_url}q={keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", attrs={"aria-label": "pagination"})
    if pagination == None:
        return 1
    pages = pagination.select("div a")
    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count

    # chrome driver version이 달라서 계속 창이 꺼지는 현상 발생시;
    # while True:
    #  pass

print(get_page_count("python"))

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("찾아야할 페이지 수 : ", pages)
    results = []
    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs?"
        final_url = f"{base_url}q={keyword}&start={page*10}"
        print(final_url)
        browser.get(final_url)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)
        # recursive 를 False 로 하면 아래 단계까지 찾는게 아니라 바로 아래 단계에서만 찾는다
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor["aria-label"]
                link = anchor["href"]
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
                job_data = {
                    'link': f"https://kr.indeed.com{link}",
                    'company': company.string,
                    'location': location.string,
                    'position': title
                }
                results.append(job_data)
    return results

jobs = extract_indeed_jobs("python")

print(jobs)



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