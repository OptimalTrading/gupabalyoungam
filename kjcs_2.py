# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import csv

# 아동학회지 크롤 시작, 국문초록 제공안함. 영문초록만 제공
article_link_list = []
for x in range(1, 2000, 1):
    r = requests.get("http://www.ibabynews.com/News/SubNewsList.aspx?PageNo="+str(x)+"&CategoryCode=0005")
    soup = BeautifulSoup(r.text, 'html.parser')
    article_key_pattern = re.compile("'(\d+)'")
    for item in soup.find_all('div', class_='SubTNL'):
        item_temp1 = item.find('h1')
        article_link_list.append(item_temp1.a['href'])
    print(x, '페이지 아티클 주소 수집중')

article_text_data = []
for index, link in enumerate(article_link_list):
    r = requests.get("http://www.ibabynews.com"+str(link))
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find("div",{"id": "divNewsTitle"}).get_text().rstrip('\n').strip()
    title = soup.find("title").get_text().rstrip('\n').strip()
    submain = soup.find("div", class_='SubMainDiv')
    text = submain.find_all("div")[11].get_text().rstrip('\n').strip()
    dateTemp = submain.find_all("div")[10]
    dateTemp2 = dateTemp.find("span",class_='Date')
    date = dateTemp2.find_all("span")[0].get_text().rstrip('\n').strip()
    text = text.rstrip('\n')
    title = title.rstrip('\n')
    title = title.replace('\n','')
    text = text.replace('\n','')
    
    print(str(index+1)+"/"+str(len(article_link_list)), "크롤링 완료")
    article_text_data.append([title, text, date])

with open("iBabyNews_김태경.csv", 'w', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['title', 'text', 'date'])
    csvwriter.writerows(article_text_data)
