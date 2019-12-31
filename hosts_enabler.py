# -*- coding: utf-8 -*-

import sqlite3
import re
import time
import CommonConfigProcessor
import CommonDBProcessor
from flask import Flask
from flask import jsonify
from flask_httpauth import HTTPBasicAuth

###############################################################################


class DBHandler(CommonDBProcessor.CommonDBProcessor):
    """数据库操作"""

    def __init__(self, database):
        super(DBHandler, self).__init__(database)

    def get_hosts(self):
        query = "SELECT * FROM hosts ORDER BY ip"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_host(self, ip):
        query = "SELECT * FROM hosts WHERE ip='%s'" %(ip)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def obsolete_hosts(self, timestamp):
        query = "UPDATE hosts SET stat='obs' WHERE timestamp < %d" %(timestamp)
        self.cursor.execute(query)
        self.conn.commit()

##############################################################################


app = Flask(__name__)

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == confprocessor.get_username():
        return confprocessor.get_password()
    else: return None

@app.route('/', methods=['GET'])
def index():
    """Introduction of platform"""
    port = confprocessor.get_port()
    return u'''<html><head><title>欢迎使用HOSTS查询平台</title></head>
               <body><h1>本平台开放以下能力</h1>
               <ul>
               <li>查询能力：[get] https://x.x.x.x:%d/query</li>
               </ul>
               </body></html>
            ''' %(port)

@app.route('/query', methods=['GET'])
def query():
    """Introduction of query function"""
    port = confprocessor.get_port()
    return u'''<html><head><title>查询能力</title></head>
               <body><h1>【查询】能力提供以下API</h1>
               <ul>
               <li>全部HOSTS状态：[get] https://x.x.x.x:%d/query/hosts</li>
               <li>某HOST状态：[get] https://x.x.x.x:%d/query/hosts/[IP]</li>
               </ul>
               </body></html>
            ''' %(port, port)

@app.route('/query/hosts', methods=['GET'])
@auth.login_required
def get_hosts():
    """Query all hosts"""
    hosts = DBHandler('hosts_explor.db').get_hosts()
    results = []
    if hosts:
        for ip, stat, timestamp in hosts:
            results.append({'ip': ip, 'stat': stat, 'timestamp': timestamp})
    return jsonify({'results': results})

@app.route('/query/hosts/<string:ip>', methods=['GET'])
@auth.login_required
def get_host(ip):
    """Query specific host"""
    results = []
    if len(ip) > 15: return jsonify({'results': results})
    ip = re.sub('[a-zA-Z_]~`!@#$%^&*()_-+={[}]|\\:;\"\'<,>?/', '', ip)
    hosts = DBHandler('hosts_explor.db').get_host(ip)
    if hosts:
        for ip, stat, timestamp in hosts:
            results.append({'ip': ip, 'stat': stat, 'timestamp': timestamp})
    return jsonify({'results': results})

@app.route('/operation/renew', methods=['POST'])
@auth.login_required
def set_renew():
    """清理过期数据"""
    deadline = -28 #days before
    deadline_time = deadline * 86400 #secs
    now_time = int(time.time())
    DBHandler('hosts_explor.db').obsolete_hosts(now_time+deadline_time)
    return jsonify({'results': 'OK'})

##############################################################################


if __name__ == '__main__':
    confprocessor = CommonConfigProcessor.CommonConfigProcessor(
        'config_hosts_explor.txt')
    app.run(
        host='0.0.0.0', port=confprocessor.get_port(), ssl_context='adhoc')

