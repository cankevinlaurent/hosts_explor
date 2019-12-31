# -*- coding: utf-8 -*-

import os
import time
import random
import subprocess
import requests
import sqlite3
import ipaddr
import CommonConfigProcessor
import CommonDBProcessor

##############################################################################


class ConfigHandler(CommonConfigProcessor.CommonConfigProcessor):

    def __init__(self, filename):
        super(ConfigHandler, self).__init__(filename)
        self._subnet_url = self._set_subnet_url()

    def _set_subnet_url(self):
        if not self._content: return None
        for line in self._content:
            if 'subnet_url' in line:
                return line.split('=')[1].strip()
        return None

    def get_subnet_url(self):
        return self._subnet_url

##############################################################################


class HostExplorer(object):
    """探测活跃host"""

    def get_subnets(self, url, auth):
        resp = requests.get(url=url, auth=auth,
            headers={'Accept': 'application/json'}, verify=False)
        if resp.status_code != 200: return None
        return resp.json()

    def resolve_subnets_to_hosts(self, json, location):
        if not json: return None
        iplist = []
        for subnet in json['results']:
            if subnet['location'] != location: continue #other area
            ips = '%s/%s' %(subnet['subnet'], subnet['netmask'])
            for ip in ipaddr.IPv4Network(ips).iterhosts(): #no broadcast ip
                ip = str(ip)
                if ip in subnet['gateways']: continue
                iplist.append(ip)
        return iplist

    def ping_ip(self, ip):
        """ping测IP是否活跃"""
        cmd= 'ping -c 3 -w 1 %s' %(ip)
        timestamp = int(time.time())
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        if b'ttl' in proc.communicate()[0]: stat = 'up'
        else: stat = 'down'
        return [(ip, stat, timestamp)]

##############################################################################


class DBHandler(CommonDBProcessor.CommonDBProcessor):

    def __init__(self, database):
        super(DBHandler, self).__init__(database)

    def write_to_db(self, result):
        self.cursor.executemany(
            'INSERT OR REPLACE INTO hosts VALUES(?,?,?)', result)
        self.conn.commit()

##############################################################################


def main():
    confhandler = ConfigHandler('config_hosts_explor.txt')

    dbhandler = DBHandler('hosts_explor.db')

    hostexplorer = HostExplorer()
    json = hostexplorer.get_subnets(
        confhandler.get_subnet_url() + '/query/subnets',
        (confhandler.get_username(), confhandler.get_password()))
    iplist = hostexplorer.resolve_subnets_to_hosts(json,
        confhandler.get_location())

    if iplist:
        random.shuffle(iplist)
        for ip in iplist:
            result = hostexplorer.ping_ip(ip)
            dbhandler.write_to_db(result)
            print result[0]
            time.sleep(10) #ping ip every 10s

##############################################################################


if __name__ == '__main__':
    while True:
        main()
        time.sleep(10)
