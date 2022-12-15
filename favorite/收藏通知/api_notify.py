import flask,json
from flask import request
from urllib.parse import unquote
import json
import telegram
import pymysql
import requests

api = flask.Flask(__name__) 
bot = telegram.Bot(token='****')
embyurl = '****'
embyapikey = '****'
#连接数据库
connect = pymysql.connect(host='****', 
                          user='****',
                          password='****',
                          db='****',
                          charset='utf8') #服务器名,账户,密码，数据库名称
db = connect.cursor()

def idtochatid(id):
    try:
        create_sqli = "SELECT chatid FROM user WHERE emby_userid = "+'"'+ str(id)+'"'
        db.execute(create_sqli)
        result = db.fetchall()
    except Exception as e:
        return(0)
    else:
        print(id)
        if(len(result) == 0):
            return(0)
        else:
            userid=result[0][0]
            return(userid)

def check_chatid_in_like(chatid):
    try:
        create_sqli = "SELECT * FROM favorite WHERE chatid =  "+'"'+ str(chatid)+'"'
        db.execute(create_sqli)
        result = db.fetchall()
    except Exception as e:
        print(e)
    else:
        if(result):
            return 1 #存在
        else:
            return 0 #不存在

def favorite_nums(chatid):
    try:
        create_sqli = "SELECT * FROM favorite WHERE chatid =  "+'"'+ str(chatid)+'"'
        db.execute(create_sqli)
        result = db.fetchall()
    except Exception as e:
        print(e)
    else:
        text = result[0][2]
        texts = str(text).split(',')
        return len(texts)

def check_allready_like(chatid,itemid):
    try:
        create_sqli = "SELECT * FROM favorite WHERE chatid =  "+'"'+ str(chatid)+'"'
        db.execute(create_sqli)
        result = db.fetchall()
    except Exception as e:
        print(e)
    else:
        check = 0
        text = result[0][2]
        texts = str(text).split(',')
        length = len(texts)
        for i in range(length):
            if(texts[i] == itemid):
                check = 1
        return check

def cancel_favourite(chatid,itemid):
    try:
        create_sqli = "SELECT * FROM favorite WHERE chatid =  "+'"'+ str(chatid)+'"'
        db.execute(create_sqli)
        result = db.fetchall()
    except Exception as e:
        print(e)
    else:
        text = result[0][2]
        texts = str(text).split(',')
        texts.remove(itemid)
        mes =  ','.join(str(i) for i in texts)

    try: 
        sql = "UPDATE favorite set fav="+'"'+str(mes)+'"'+" where chatid="+str(chatid)
        print(sql)
        db.execute(sql)
        connect.commit()
    except Exception as e:
        print(e)
    else:
        return 1

def add_favourite(chatid,itemid):
    try:
        create_sqli = "SELECT * FROM favorite WHERE chatid =  "+'"'+ str(chatid)+'"'
        db.execute(create_sqli)
        result = db.fetchall()
    except Exception as e:
        print(e)
    else:
        text = result[0][2]
        texts = str(text).split(',')
        texts.append(itemid)
        mes =  ','.join(str(i) for i in texts)

    try: 
        sql = "UPDATE favorite set fav="+'"'+str(mes)+'"'+" where chatid="+str(chatid)
        print(sql)
        db.execute(sql)
        connect.commit()
    except Exception as e:
        print(e)
    else:
        return 1

def server_add(embyid,itemid,chatid):
    headers = {
        'accept': 'application/json',
    }

    params = {
        'api_key': embyapikey,
    }

    response = requests.post(embyurl + 'emby/Users/'+embyid+'/FavoriteItems/'+itemid, params=params, headers=headers)

    try: 
        sql = "UPDATE favorite set locked=1 where chatid="+str(chatid)
        print(sql)
        db.execute(sql)
        connect.commit()
    except Exception as e:
        print(e)
    else:
        return 1

def server_cancel(embyid,itemid,chatid):
    headers = {
        'accept': 'application/json',
    }

    params = {
        'api_key': embyapikey,
    }

    response = requests.delete(embyurl + 'emby/Users/'+embyid+'/FavoriteItems/'+itemid, params=params, headers=headers)

    try: 
        sql = "UPDATE favorite set locked=1 where chatid="+str(chatid)
        print(sql)
        db.execute(sql)
        connect.commit()
    except Exception as e:
        print(e)
    else:
        return 1
            

@api.route('/update',methods=['post'])
def update():
    data = request.get_data()
    data_decode = unquote(str(data,encoding='utf-8'))
    split = data_decode.split('\n')
    datajson = json.loads(split[4])
    emby_id = datajson["User"]["Id"]
    item_id = datajson["Item"]["Id"]
    item_name = datajson["Item"]["Name"]
    item_type = datajson["Item"]["Type"]
    print(emby_id,item_id,item_name,item_type)
    chatid = idtochatid(emby_id)
    check_exist = check_chatid_in_like(chatid)
    if(item_type == 'Series'):
        if(check_exist == 0):
            try: 
                sql = "insert into favorite (chatid,emby_userid,fav,locked) values ("+str(chatid)+","+'"'+str(emby_id)+'"'+","+'"'+str(item_id)+'"'+",0)"
                print(sql)
                db.execute(sql)
                connect.commit()
            except Exception as e:
                print(e)
            else:
                server_add(emby_id,item_id,chatid)
                message = "[Emby公益服]"+item_name+"：收藏成功"
                bot.send_message(chat_id=chatid, text=message)
        elif(check_exist == 1):
            check_like = check_allready_like(chatid,item_id)
            try:
                create_sqli = "SELECT * FROM favorite WHERE chatid =  "+'"'+ str(chatid)+'"'
                db.execute(create_sqli)
                result = db.fetchall()
            except Exception as e:
                print(e)
            else:
                lock = result[0][3]
            if(lock == '0'):
                if(check_like == 0):
                    back = add_favourite(chatid,item_id)
                    server_add(emby_id,item_id,chatid)
                    if(back == 1):
                        message = "[Emby公益服]"+item_name+"：收藏成功"
                        bot.send_message(chat_id=chatid, text=message)
                elif(check_like == 1):
                    back = cancel_favourite(chatid,item_id)
                    server_cancel(emby_id,item_id,chatid)
                    if(back == 1):
                        message = "[Emby公益服]"+item_name+"：取消收藏成功"
                        bot.send_message(chat_id=chatid, text=message)
            else:
                try: 
                    sql = "UPDATE favorite set locked=0 where chatid="+str(chatid)
                    print(sql)
                    db.execute(sql)
                    connect.commit()
                except Exception as e:
                    print(e)
                else:
                    print("skip!")
                    
    return('200')
  
if __name__ == '__main__':
    api.run(port=12345,debug=True,host='0.0.0.0') 