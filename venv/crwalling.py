import requests
import pymysql
import re
import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

# 디비연결
conn = pymysql.connect(host='115.68.177.249', user='e3hope', password='ds64079376*', db='SN', charset='utf8')
cursor = conn.cursor()

# 변수할당
data = []

# 크롤링
webpage = requests.get('https://www.fmkorea.com/index.php?mid=football_news')
soup = BeautifulSoup(webpage.content, 'html.parser')

# 최근 업데이트 목록 호출
# sql = 'select title from Scrap ORDER BY idx DESC LIMIT 1'
# cursor.execute(sql)
# result = cursor.fetchone()

# 데이터 정리
data = soup.select('tr:not(.notice)')
del data[0]
insert_data = []

#데이터 추출
for d in data :
    if re.search(':',str(d.select('.time'))) :
        date = datetime.datetime.now()
        temp = []

        # 전날 계산
        # if d.select_one('.time').get_text().replace('\t', '') >= date.strftime('%H:%m') :
        #     date = date - timedelta(1)

        # 1시간 주기로 크롤링
        if (datetime.datetime.now() - datetime.timedelta(hours = 1)).strftime('%H:%m') > d.select_one('.time').get_text().replace('\t', '') :
            temp.append(d.select_one('.hotdeal_var8 > a').get_text().replace('\t', ''))
            temp.append(d.select_one('.hotdeal_var8 > a')['href'])
            temp.append(date.strftime('%Y-%m-%d') + ' ' + d.select_one('.time').get_text().replace('\t', ''))
            insert_data.append(temp)
        # 입력한 데이터일 경우 추가 X
        # if result[0] in d.select_one('.hotdeal_var8 > a').get_text() :

#데이터 입력
for insert in reversed(insert_data) :
    sql = 'INSERT INTO Scrap (title,link,date) VALUES(%s,%s,%s)'
    cursor.execute(sql, (insert))
    conn.commit()
conn.close()