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
num = 1000000
while(num<100000000):
    url = 'https://api.douban.com/v2/note/user_created/'+str(num)
    #heade = {'apikey': '116cac245911274a9921658b1ddea6ad'}
    #req = urllib2.Request(url, headers= heade)
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    resp = json.load(resp)
    content = json.dumps(resp, ensure_ascii= False)
    if(content):
        print(content)
    if(resp['total']!=0):
        userId = resp['user']['id']
        nodeId = resp['notes'][0]['id']
        name = resp['user']['name']
        title = str(resp['notes'][0]['title'].encode('utf-8'))
        summary = str(resp['notes'][0]['summary'].encode('utf-8'))
        content = str(resp['notes'][0]['content'].encode('utf-8'))
        comments = int(resp['notes'][0]['comments_count'])
        liked = int(resp['notes'][0]['liked_count'])
        up = resp['notes'][0]['update_time']
        update = datetime.datetime.strptime(up, "%Y-%m-%d %H:%M:%S")
        pu = resp['notes'][0]['publish_time']
        publish = datetime.datetime.strptime(pu, "%Y-%m-%d %H:%M:%S")
        print(title)
        # 打开数据库连接
        db = MySQLdb.connect("localhost","root","123","doubanapi" ,charset='utf8')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行sql语句
        cursor.execute('insert into doubannote(note_id, user_id,user_name,title,summary,content,comments_count,'
                       'liked_count,update_time,publish_time) '
                       'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (nodeId, userId, name, title, summary, content, comments, liked, update, publish))
        # 提交到数据库执行
        db.commit()

        # 关闭数据库连接
        db.close()
    num = num+1
    time.sleep(10)