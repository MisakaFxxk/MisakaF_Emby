import flask,requests,json,urllib
from flask import request,jsonify
from urllib.parse import unquote
from urllib.parse import urlencode

#全局变量
localhost = ''  #本地Emby地址，未经过Nginx的Emby访问链接，最后不加/
embyurl = ''    #外部Emby地址，用户最终访问的Emby链接，最后加/

#Flask服务
api = flask.Flask(__name__) 
api.config['JSON_SORT_KEYS'] = False

@api.route('/emby/Users/<user_id>/Items/<item_id>', methods=["GET", "POST"])
def update(user_id,item_id):
    host_url = embyurl
    UA = request.user_agent
    client_name = request.args.get("X-Emby-Client")
    device_name = request.args.get("X-Emby-Device-Name")
    device_id = request.args.get("X-Emby-Device-Id")
    ver = request.args.get("X-Emby-Client-Version")
    token = request.args.get("X-Emby-Token")
    headers = {
        'Host': '127.0.0.1',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN',
        'User-Agent': str(UA),
        'accept': 'application/json',
    }

    params = {
        'X-Emby-Client': client_name,
        'X-Emby-Device-Name': device_name,
        'X-Emby-Device-Id': device_id,
        'X-Emby-Client-Version': ver,
        'X-Emby-Token': token,
    }
    try:
        response = requests.get(localhost + '/emby/Users/'+user_id+'/Items/'+item_id + '?' +urlencode(params))
        restext = response.text
        resjson = json.loads(restext)
    except Exception as e:
        print(e,"error，请重新访问")
    else:
        try:
            #获取播放链接
            source_num = len(resjson["MediaSources"])
            pot_url = []
            nplayer_url = []
            iina_url = []
            infuse_url = []
            media_name = []
            sub_url = ''
            for i in range(source_num):
                type = resjson["MediaSources"][i]["Container"]
                media_id = resjson["MediaSources"][i]["Id"]
                media_name.append(resjson["MediaSources"][i]["Name"])
                #获取播放流
                domain = host_url + "emby/videos/"+item_id
                url = domain+"/stream."+type+'?'
                paramsurl = {
                    "api_key":token,
                    "Static":"true",
                    "MediaSourceId":media_id
                }
                stream_url =  url + urlencode(paramsurl)
                #获取字幕流
                stream_num = len(resjson["MediaStreams"])
                for j in range(stream_num):
                    stream_type = resjson["MediaStreams"][j]["Type"]
                    IsExternal = resjson["MediaStreams"][j]["IsExternal"]
                    if(stream_type == "Subtitle" and IsExternal == True):
                        stream_language = resjson["MediaStreams"][j]["Language"]
                        if("chs" in stream_language):        
                            sub_id = resjson["MediaStreams"][j]["Index"]
                            sub_codec = resjson["MediaStreams"][j]["Codec"]
                            sub_url = domain + "/" + str(media_id) + "/Subtitles/" + str(sub_id) + "/Stream." + str(sub_codec) + "?api_key=" +str(token)
                pot_url.append("potplayer://" + stream_url + " /sub=" + sub_url)
                nplayer_url.append("nplayer-" + stream_url)
                iina_url.append("iina://weblink?url=" + urllib.parse.quote(stream_url) + "%26new_window=1%26Static=true")
                infuse_url.append(host_url + "redirect2player?infuseurl=infuse://x-callback-url/play?url=" + urllib.parse.quote(stream_url))
        except Exception as e:
            print("非播放页面，跳过",e)
            resjson = json.dumps(resjson,ensure_ascii=False,sort_keys=False)
            print("-"*20)
            return resjson,200,{"Content-Type":"application/json; charset=utf-8","Access-Control-Allow-Headers": "Accept, Accept-Language, Authorization, Cache-Control, Content-Disposition, Content-Encoding, Content-Language, Content-Length, Content-MD5, Content-Range, Content-Type, Date, Host, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, Origin, OriginToken, Pragma, Range, Slug, Transfer-Encoding, Want-Digest, X-MediaBrowser-Token, X-Emby-Token, X-Emby-Client, X-Emby-Client-Version, X-Emby-Device-Id, X-Emby-Device-Name, X-Emby-Authorization","Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS","Access-Control-Allow-Origin": "*"}
        else:
            #追加外部播放器链接至json内
            temp = resjson[ 'ExternalUrls' ]
            for i in range(source_num):
                pot_add = {"Name":'PotPlayer - ' + media_name[i],"Url":pot_url[i]}
                nplayer_add = {"Name":'nPlayer - ' + media_name[i],"Url":nplayer_url[i]}
                iina_add = {"Name":'IINA - ' + media_name[i],"Url":iina_url[i]}
                infuse_add = {"Name":'Infuse - ' + media_name[i],"Url":infuse_url[i]}
                temp.append(iina_add)
                temp.append(pot_add)
                temp.append(nplayer_add)
                temp.append(infuse_add)
            resjson = json.dumps(resjson,ensure_ascii=False,sort_keys=False)
            print("-"*20)
            return resjson,200,{"Content-Type":"application/json; charset=utf-8","Access-Control-Allow-Headers": "Accept, Accept-Language, Authorization, Cache-Control, Content-Disposition, Content-Encoding, Content-Language, Content-Length, Content-MD5, Content-Range, Content-Type, Date, Host, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, Origin, OriginToken, Pragma, Range, Slug, Transfer-Encoding, Want-Digest, X-MediaBrowser-Token, X-Emby-Token, X-Emby-Client, X-Emby-Client-Version, X-Emby-Device-Id, X-Emby-Device-Name, X-Emby-Authorization","Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS","Access-Control-Allow-Origin": "*"}


if __name__ == '__main__':
    api.run(port=12345,debug=False,host='0.0.0.0') 