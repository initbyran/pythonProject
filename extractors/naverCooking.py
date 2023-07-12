
import requests
from bs4 import BeautifulSoup
import time

def extractors_naver_cooking():
    base_url = "https://terms.naver.com"
    category_url = "https://terms.naver.com/list.naver?cid=63025&categoryId=63777&page="

    page_num = 1
    results = []
    cnt = 0
    while cnt <= 250:
        response = requests.get(category_url + str(page_num))
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if we are on the last page
        if not soup.select('.list_wrap'):
            break

        # Get the list of entries on the page
        for entry in soup.select('.list_wrap > ul > li'):
            title = entry.select_one('.subject .title').text.strip()
            link = base_url + entry.select_one('a')['href']

            # Visit the page for the entry
            entry_response = requests.get(link)
            entry_soup = BeautifulSoup(entry_response.text, 'html.parser')

            # Get the date and content
            content = entry_soup.select_one('#size_ct').text.strip() if entry_soup.select_one('#size_ct') is not None else "Unknown"

            title = title.replace('\n','')
            title = title.replace('\t','')
            title = title.replace('  ', '')
            title = title.replace('담기', '')
            content = content.replace('\n','')
            content = content.replace('\t', '')
            content = content.replace('  ', '')
            content = content.replace('이미지 크게보기', '')

            cooking_data = {
                'title' : title,
                'content' : content
            }
            results.append(cooking_data)
        print(title)
        print(f'/////{cnt}//////')
        page_num += 1
        time.sleep(1)  # Sleep for a while to not overload the server
        cnt = cnt +1

    return results
