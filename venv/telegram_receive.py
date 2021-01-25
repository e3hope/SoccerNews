import telegram
import pymysql

#bot을 선언
my_token = '1528268221:AAFJZkjDJT_Mw21OAnupbMrX4rSLgc0reJk'
bot = telegram.Bot(token = my_token)

# 디비 연결
conn = pymysql.connect(host='localhost', user='e3hope', password='ds64079376*', db='SN', charset='utf8')
cursor = conn.cursor()

# 마지막 업데이트목록
lastupdatesql = 'SELECT update_id FROM Lastupdate'
cursor.execute(lastupdatesql)
offset = cursor.fetchone()

#업데이트
updates = bot.getUpdates(offset=offset[0])

# 데이터 입력
for u in updates :
    
    # 남아있는 데이터 넘기기
    if u['update_id'] == offset[0] :
        continue

    # 회원 입력
    if u.message.text == '/start' :
        sql = 'INSERT INTO User (chat_id, id, name, date) VALUES(%s, %s, %s, now()) ON DUPLICATE KEY UPDATE date = now()'
        cursor.execute(sql, (u.message.chat.id, u.message.chat.username, u.message.chat.last_name + u.message.chat.first_name))
        bot.sendMessage(chat_id = u.message.chat.id, text = '/help를 눌러 도움말을 확인하세요.')
        conn.commit()

    # 키워드 입력
    elif u.message.text.startswith('@') :
        sql = 'UPDATE User SET keyword = %s WHERE chat_id = %s'
        cursor.execute(sql,(u.message.text.replace('@', ''), u.message.chat.id))
        bot.sendMessage(chat_id=u.message.chat.id, text = 'keyword가 "' + u.message.text.replace('@', '') + '"로 변경되었습니다.')
        conn.commit()

    # 도움말
    elif u.message.text == '/help' :
        bot.sendMessage(chat_id=u.message.chat.id, text='@keyword를 입력해 주세요. ex)@리버풀\n'
                        '|입력시 다른기사도 확인 할 수 있습니다. ex)@리버풀|맨유\n'
                        '/link입력시 기사의 원문 링크도 확인 할 수 있습니다.')

    # 기사링크 활성화/비활성화
    elif u.message.text == '/link' :
        sql = 'UPDATE User SET link = 1 - link WHERE chat_id = %s'
        cursor.execute(sql, (u.message.chat.id))
        bot.sendMessage(chat_id=u.message.chat.id, text='링크상태가 변경되었습니다.')
        conn.commit()

# 메세지 저장
if updates :
    updatesql = 'UPDATE Lastupdate SET update_id = %s'
    cursor.execute(updatesql, updates[-1]['update_id'])
    conn.commit()
conn.close()