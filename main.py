# from extractors.indeed import extract_indeed_jobs
# from extractors.wwr import extract_wwwr_jobs
#
# keyword = input("What do you wnat to search for?")
#
# indeed = extract_indeed_jobs(keyword)
# wwr = extract_wwwr_jobs(keyword)
#
# jobs = indeed + wwr
#
# file = open(f"{keyword}.csv", "w", encoding='utf-8')
# file.write("Position,Company,Location,URL\n")
#
# for job in jobs:
#     file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n")
#
# file.close()


# 네이버
from extractors.naverTravel import extractors_naver_travel
import json

info = extractors_naver_travel()

results = []

print("processing data to json")

# json 형태 저장하는걸 바꾸려면 여기수정
for contents in info:
    results.append({
        'document' : f"{contents['title']} : {contents['content']}"
    })

# json 저장
with open('news1post-travel.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent="\t")

print(len(results))


# # 그랑라루스 요리백과
# from extractors.naverCooking import extractors_naver_cooking
# import json
#
# cooking_info = extractors_naver_cooking()
#
# results = []
#
# print("processing data to json")
#
# # json 형태 저장하는걸 바꾸려면 여기수정
# for cooking in cooking_info:
#     results.append({
#         'document' : f"{cooking['title']} : {cooking['content']}"
#     })
#
# # json 저장
# with open('larousse-food.json', 'w', encoding='utf-8') as f:
#     json.dump(results, f, ensure_ascii=False, indent="\t")
#
# print(len(results))



