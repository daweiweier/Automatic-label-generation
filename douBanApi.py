# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 10:37:20 2016
@author: wyw
"""
import urllib2
import json
import MySQLdb
import datetime
import time
num = 1000181
while(num<100000000):
    url = 'https://api.douban.com/v2/note/user_created/'+str(num)
    req = urllib2.Request(url)
    try:
        resp = urllib2.urlopen(req)
        resp = json.load(resp)
        content = json.dumps(resp, ensure_ascii= False)
        cnt = resp['total']
        varnum = 0
        if(cnt>20):
            cnt = 20
        if(content):
            print(content)
        while(resp['total']!=0 & varnum<cnt):
            # 打开数据库连接
            db = MySQLdb.connect("localhost","root","123","doubanapi" ,charset='utf8')
            saveNote(db)
            # 关闭数据库连接
            db.close()
            varnum = varnum+1
    except:
        print("no user...")
    num = num+1
    time.sleep(10)

    def saveNote(db):
        userId = resp['user']['id']
        nodeId = resp['notes'][varnum]['id']
        name = resp['user']['name']
        title = str(resp['notes'][varnum]['title'].encode('utf-8'))
        summary = str(resp['notes'][varnum]['summary'].encode('utf-8'))
        content = str(resp['notes'][varnum]['content'].encode('utf-8'))
        comments = int(resp['notes'][varnum]['comments_count'])
        liked = int(resp['notes'][varnum]['liked_count'])
        up = resp['notes'][varnum]['update_time']
        update = datetime.datetime.strptime(up, "%Y-%m-%d %H:%M:%S")
        pu = resp['notes'][varnum]['publish_time']
        publish = datetime.datetime.strptime(pu, "%Y-%m-%d %H:%M:%S")

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行sql语句
        cursor.execute('insert into doubannote(note_id, user_id,user_name,title,summary,content,comments_count,'
                       'liked_count,update_time,publish_time) '
                       'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (nodeId, userId, name, title, summary, content, comments, liked, update, publish))
        # 提交到数据库执行
        db.commit()
