from urllib.parse import unquote
import sys
import telegram,pymysql


bot = telegram.Bot(token='****')
#连接数据库
connect = pymysql.connect(host='****',
                          user='****',
                          password='****',
                          db='****',
                          charset='utf8') #服务器名,账户,密码，数据库名称
db = connect.cursor()


itemid = sys.argv[1]
itemname = sys.argv[2]
season_num = sys.argv[3]
episode_num = sys.argv[4]
print(itemid,itemname,season_num,episode_num)
try:
    create_sqli = "SELECT * FROM favorite "
    db.execute(create_sqli)
    result = db.fetchall()
except Exception as e:
    print(e)
else:
    length =  len(result)
    for i in range(length):
        fav_items = result[i][2]
        chatid = result[i][0]
        favs = str(fav_items).split(',')
        fav_length = len(favs)
        for num in range(fav_length):
            if(favs[num] == itemid):
                message = "[Emby]您订阅的剧集：" + itemname+"更新至S"+season_num+"E"+episode_num
                bot.send_message(chat_id=chatid, text=message)
                print(chatid + "    send")
                break

  