import flask,requests,json,pymysql
from flask import request
from DBUtils.PooledDB import PooledDB
from pymysql.converters import escape_string

api = flask.Flask(__name__) 
localhost = 'http://127.0.0.1:8096' #本地Emby地址，未经过Nginx的Emby访问链接，最后不加/

#连接数据库
DB_CONFIG={
    "host":"127.0.0.1",
    "port":3306,
    "user":"",
    "password":"",
    "db":"infuse",
    "charset":"utf8"
}

#创建Mysql线程池
class MysqlTools(object):
    def __init__(self):
        self.pool=PooledDB(
            creator=pymysql,
            maxconnections=10, #连接池允许的最大连接数
            mincached=1,
            maxcached=5,
            maxshared=3,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=0,
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["db"],
            charset=DB_CONFIG["charset"]
        )

    def open(self):
        conn=self.pool.connection()
        cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
        return conn,cursor

    def close(self,conn,cursor):
        cursor.close()
        conn.close()

    def get_list(self, sql, args=None):
        try:
            conn,cursor=self.open()
            cursor.execute(sql, args)
            result = cursor.fetchall()
            self.close(conn,cursor)
            return result
        except:
            return False

    # 查询单条记录
    def get_one(self, sql, args=None):
        try:
            conn, cursor = self.open()
            cursor.execute(sql, args)
            result = cursor.fetchone()
            self.close(conn, cursor)
            return result
        except:
            return False

    # 执行单条sql
    def execute_one(self, sql, args=None):
        try:
            conn, cursor = self.open()
            cursor.execute(sql, args)
            conn.commit()
            self.close(conn, cursor)
            return True
        except Exception as e:
            print(e)
    
    # 添加数据返回insertID
    def create(self, sql, args=None):
        try:
            conn, cursor = self.open()
            cursor.execute(sql, args)
            conn.commit()
            insert_id = cursor.lastrowid
            self.close(conn, cursor)
            return insert_id
        except:
            self.close(conn, cursor)
            return False

    def close(self,conn,cursor):
        try:

            cursor.close()
            conn.close()
        except:
            raise Exception("关闭数据库失败")


@api.route('/Users/<user_id>/Items', methods=["GET", "POST"])
def update(user_id):
    my_mysql=MysqlTools()
    #参数获取
    ParentId = request.args.get("ParentId")
    StartIndex = request.args.get("StartIndex")
    Limit = request.args.get("Limit")
    IncludeItemTypes = request.args.get("IncludeItemTypes")
    UserAgent = request.user_agent
    XEmbyAuthorization = request.headers.get('X-Emby-Authorization')

    #判断是否为新数据
    exist = 0
    try: 
        sql = "select count(*) from metadata where ParentId = {ParentId} and StartIndex = {StartIndex} and IncludeItemTypes = '{IncludeItemTypes}'".format(ParentId=ParentId,StartIndex=StartIndex,IncludeItemTypes=IncludeItemTypes)
        result = my_mysql.get_one(sql)
    except Exception as e:
        print(e,"flag1")
    else:
        exist = result["count(*)"]
    if(exist == 0):
        #新数据请求
        print("未命中，写入数据库")
        headers = {
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': str(UserAgent),
            'Accept': 'application/json',
            'X-Emby-Authorization': str(XEmbyAuthorization)
        }
        url = localhost + '/Users/{user_id}/Items?ExcludeLocationTypes=Virtual&Fields=DateCreated,Etag,Genres,MediaSources,Overview,ParentId,Path,People,ProviderIds,SortName,CommunityRating,OfficialRating,PremiereDate&ParentId={ParentId}&StartIndex={StartIndex}&Limit={Limit}&IncludeItemTypes={IncludeItemTypes}&Recursive=true'.format(user_id=user_id,ParentId=ParentId,StartIndex=StartIndex,Limit=Limit,IncludeItemTypes=IncludeItemTypes)
        response = requests.get(url,headers=headers)
        resjson = response.json()

        try:
            #向Infuse客户端返回
            return resjson,200,{"Content-Type":"application/json; charset=utf-8","Access-Control-Allow-Headers": "Accept, Accept-Language, Authorization, Cache-Control, Content-Disposition, Content-Encoding, Content-Language, Content-Length, Content-MD5, Content-Range, Content-Type, Date, Host, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, Origin, OriginToken, Pragma, Range, Slug, Transfer-Encoding, Want-Digest, X-MediaBrowser-Token, X-Emby-Token, X-Emby-Client, X-Emby-Client-Version, X-Emby-Device-Id, X-Emby-Device-Name, X-Emby-Authorization","Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS","Access-Control-Allow-Origin": "*"}
        finally:
            #判断是否为不完整数据
            length = len(resjson["Items"])
            if length == 200:
                #完整数据，向数据库追加新数据
                data = json.dumps(resjson,ensure_ascii=False)
                try: 
                    sql = "insert into metadata (ParentId,StartIndex,IncludeItemTypes,data) values ({ParentId},{StartIndex},'{IncludeItemTypes}','{data}')".format(ParentId=ParentId,StartIndex=StartIndex,IncludeItemTypes=IncludeItemTypes,data=escape_string(data))
                    result = my_mysql.create(sql)
                except Exception as e:
                    print(e,"flag2")
            else:
                #非完整数据，不导入数据库
                print("数据不完整，skip!")     
    else:
        #数据库中已存在
        print("命中")
        try: 
            sql = "select data from metadata where ParentId = {ParentId} and StartIndex = {StartIndex} and IncludeItemTypes = '{IncludeItemTypes}'".format(ParentId=ParentId,StartIndex=StartIndex,IncludeItemTypes=IncludeItemTypes)
            result = my_mysql.get_one(sql)
        except Exception as e:
            print(e,"flag3")
        else:
            data = result["data"]
            resjson = json.loads(data)   
             #向Infuse客户端返回
            return resjson,200,{"Content-Type":"application/json; charset=utf-8","Access-Control-Allow-Headers": "Accept, Accept-Language, Authorization, Cache-Control, Content-Disposition, Content-Encoding, Content-Language, Content-Length, Content-MD5, Content-Range, Content-Type, Date, Host, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, Origin, OriginToken, Pragma, Range, Slug, Transfer-Encoding, Want-Digest, X-MediaBrowser-Token, X-Emby-Token, X-Emby-Client, X-Emby-Client-Version, X-Emby-Device-Id, X-Emby-Device-Name, X-Emby-Authorization","Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS","Access-Control-Allow-Origin": "*"}
        

if __name__ == '__main__':
    api.run(port=60000,debug=True,host='0.0.0.0',threaded=True) 
