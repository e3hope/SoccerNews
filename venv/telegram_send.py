import telegram
import pymysql
import re

#bot을 선언
my_token = '1528268221:AAFJZkjDJT_Mw21OAnupbMrX4rSLgc0reJk'
bot = telegram.Bot(token = my_token)

# 디비 연결
conn = pymysql.connect(host='115.68.177.249', user='e3hope', password='ds64079376*', db='SN', charset='utf8')
cursor = conn.cursor()

# 데이터 확인
usersql = 'SELECT chat_id, keyword, last_idx, link FROM User'
cursor.execute(usersql)
userresult = cursor.fetchall()

# 데이터 전송
for u in userresult :

    # 공백 제거
    keyword = u[1].replace('\s', '')

    if keyword :
        operator = keyword.split('/\&|\|/')  # 특수문자
        keyword = re.findall('[ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9]+', keyword);

    # sql에 맞게 키워드 정리
    if keyword :
        insert_data = [u[2]]
        for i in range(0,len(keyword)) :
            if i == 0 :
                sql = ' and ( title regexp %s'
                insert_data.append(keyword[0])
            else :
                insert_data.append(keyword[1])
                sql += (' and' if operator[i-1] == '&' else ' or') + ' title regexp %s'

        # 기사 보내기
        scrapsql = 'SELECT title, link FROM Scrap WHERE idx > %s' + sql + ')'
        cursor.execute(scrapsql, (insert_data))
        result = cursor.fetchall()
        for r in result :
            bot.sendMessage(chat_id=u[0], text=r[0] + (('\nhttps://www.fmkorea.com' + r[1]) if u[3] == 1 else '' ))

# 확인한 idx 업데이트
updatesql = 'UPDATE User SET last_idx = (SELECT idx FROM Scrap ORDER BY idx DESC limit 1)'
cursor.execute(updatesql)
conn.commit()
conn.close()