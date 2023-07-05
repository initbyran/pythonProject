from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from requests import get

def get_page_count(keyword):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options)

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



def extract_indeed_jobs(keyword):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options)

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
                    'link': f"https://kr.indeed.com/{link}",
                    'company': company.string,
                    'location': location.string,
                    'position': title
                }
                results.append(job_data)
    return results
