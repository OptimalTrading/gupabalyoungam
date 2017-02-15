# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import http.client
import urllib
import csv

# 한국교원연구 크롤 시작, 국문초록 제공안함. 영문초록만 제공
article_link_list = []
for x in range(2016, 2015, -1):
    #r = requests.get("http://www.ibabynews.com/News/SubNewsList.aspx?PageNo="+str(x)+"&CategoryCode=0005")
    r = requests.get("http://www.riss.kr/search/series/ChangeVolumeAjax.do?s_control_no=a1b7c94988b5595effe0bdc3ef48d419&publish_date="+str(x)+"&inside_outside=1")
    soup = BeautifulSoup(r.text)
    for item in soup.find_all('volumebean'):
        itemp_temp1 = item.find('v_control_no')
        article_link_list.append(itemp_temp1.get_text())
    print(x, '년도 논문집 정보 수집 중')

paper_link_list = []
#논문집 id 각각 불러와서 호출...
for index, link in enumerate(article_link_list):
    r = requests.post("http://www.riss.kr/search/series/VolumeListAjax.do?_mat_type=3a11008f85f7c51d&s_control_no=a1b7c94988b5595effe0bdc3ef48d419&v_control_no="+str(link)+"&currentPage=1&inside_outside=1&")
    soup = BeautifulSoup(r.text)
    #논문집 논문 id 각각호출 및 저장
    for item in soup.find_all('articlelist'):
        item_temp = item.find('a_control_no')
        paper_link_list.append(item_temp.get_text())


paper_text_data = []
#논문 id가 담긴 list 이용하여 논문 정보 호출
for index, link in enumerate(paper_link_list):
    try:
        s = requests.Session()
        s.post('http://www.riss.kr/search/detail/DetailView.do', data = {'p_mat_type' : '1a0202e37d52c72d', 'control_no' : str(link)})
        r =  s.post('http://www.riss.kr/search/detail/DetailView.do', data = {'p_mat_type' : '1a0202e37d52c72d', 'control_no' : str(link)})
        soup = BeautifulSoup(r.text, 'html.parser')

        #제목
        title = soup.find('div', class_='vTop02')
        title = title.find('p', class_='tit').get_text().rstrip('\n').strip()

        #초록
        abstract = soup.find('div', class_='tt').find_all('li')[1].get_text().rstrip('\n').strip()
    
        #날짜
        date = soup.find('div', class_='cont').find('ul', class_='report').find_all('li')
        for temp in date:
            tempStr = temp.find('strong').get_text()
            if(tempStr =='발행년도'):
                date = temp.find('p').get_text().rstrip('\n').strip()
                break;
        print(str(index+1)+"/"+str(len(paper_link_list)), "크롤링 완료")
        paper_text_data.append([index, title, abstract, date])
    except:
        print(str(index+1)+"/"+str(len(paper_link_list)), "크롤링 실패 ## ")
        continue

with open("riss_김태경.csv", 'w', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['index', 'title', 'abstract', 'date'])
    csvwriter.writerows(paper_text_data)










