# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import csv

# 아동학회지 크롤 시작, 국문초록 제공안함. 영문초록만 제공
article_link_list = []
for x in range(2016, 2005, -1):
    r = requests.get("http://kiss.kstudy.com/journal/list_name.asp?key1=2610&key2=3070&startCount=0&pageScale=1000&sort=&selVOL1=ALL&selNUM1=ALL&selYEAR="+str(x))
    soup = BeautifulSoup(r.text, 'html.parser')
    article_key_pattern = re.compile("'(\d+)'")
    for item in soup.find_all('li', class_='title'):
        print(item)
        article_link_list.append(article_key_pattern.search(item.a['href']).group(1))
    print(x, '년도 아티클 주소 수집중')

article_text_data = []
for index, link in enumerate(article_link_list):
    r = requests.get("http://kiss.kstudy.com/journal/thesis_name.asp?key="+str(link))
    soup = BeautifulSoup(r.text, 'html.parser')
    agency_box = soup.find("div", class_="agency_box")
    title = agency_box.find("span", class_="h3").get_text()
    author = agency_box.find_all("li")[0].get_text()
    issuedate = agency_box.find_all("li")[1].get_text().strip()
    keyword = soup.find_all("div", class_="detail")[2].find("li", class_="text").get_text()
    abstract = soup.find_all("div", class_="detail")[3].find_all("li", class_="text_2")[1].get_text()
    print(str(index+1)+"/"+str(len(article_link_list)), link, title, "크롤링 완료")
    article_text_data.append([link, title, author, issuedate, abstract, keyword])

with open("유아교육연구_김태경.csv", 'w', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['link', 'title', 'author', 'issuedate', 'abstract', 'keyword'])
    csvwriter.writerows(article_text_data)
