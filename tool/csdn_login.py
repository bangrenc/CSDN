# -*- coding: utf-8 -*-
__author__ = 'Byron'

import requests
import re

username = 'XXX'
password = 'XXX'

session = requests.Session()

url = 'http://passport.csdn.net/account/login'
Headers = {
        'Host': 'passport.csdn.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    }

response = session.get(url, headers=Headers)
lt = re.findall(r'name="lt" value="(.*)\"', response.text)[0]
execution = re.findall(r'name="execution" value="(.*)\"', response.text)[0]
post_data = {
    'username': username,
    'password': password,
    'lt': lt,
    'execution': execution,
    '_eventId': 'submit',
}


def login():
    session.post(url=url, data=post_data, headers=Headers)
    return session


if __name__=='__main__':
    session = login()
    home_page = 'http://my.csdn.net/my/mycsdn'
    resp = session.get(home_page, headers='')
    #print(resp.text)
    f = open('test.txt', 'w+')
    f.write(resp.text)
    pass



