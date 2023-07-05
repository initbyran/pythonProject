from requests import get
from bs4 import BeautifulSoup

def extract_wwwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?utf8=✓&term="
    # f = format
    response = get(f"{base_url}{keyword}")

    if response.status_code != 200:
        print("Can't request website")

    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        # class는 변수명이 될 수 없는 것이므로 '_'를 사용하여 구분해준 것
        jobs = soup.find_all('section', class_="jobs")

        # print(len(jobs))
        # len : list나 tuple의 크기

        for job_section in jobs:
            job_posts = job_section.find_all('li')
            # 'view all' 삭제
            job_posts.pop(-1)

            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                link = anchor['href']
                # list의 크기를 알고 있을 때, 변수 선언하는 방법
                company, kind, region = anchor.find_all('span', class_="company")
                # find_all : 모두 찾기
                # find : 하나만 찾기
                title = anchor.find('span', class_='title')
                # 문자만 추출해서 dictionary에 저장
                job_data = {
                    'link' : f"https://weworkremotely.com/{link}",
                    'company': company.string,
                    'region': region.string,
                    'position': title.string
                }

                results.append(job_data)
        return results
