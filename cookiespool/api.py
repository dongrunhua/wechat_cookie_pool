import json
from flask import Flask, g
from pprint import pprint
from cookiespool.config import *
from cookiespool.db import *

__all__ = ['app']

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'


def get_conn():
    """
    获取
    :return:
    """
    for website in GENERATOR_MAP:

        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts", "' + website + '")'))

    return g


@app.route('/<website>/random')
def random(website):
    """
    顺序获取Cookie, 访问地址如 /weibo/random
    :return: Cookie
    """
    g = get_conn()

    # 获取所有cookie
    cookies = getattr(g, website + '_cookies').all()
    cookies_count = []

    for index,(k,v) in enumerate(cookies.items()):
        v = eval(v)
        cookies_count.append({'name':k,'count':int(v.get('count')) if v.get('count') else 0})
    # 根据count排序
    cookies_count = sorted(cookies_count, key=lambda e: e['count'], reverse=False)
    cookie_name = cookies_count[0]['name']
    cookie_count = cookies_count[0]['count']

    cookies = getattr(g, website + '_cookies').get(cookie_name)
    # 删掉cookie
    getattr(g, website + '_cookies').delete(cookie_name)
    # 新增cookie
    new_cookie = eval(cookies)
    new_cookie['count'] = str(cookie_count+1)
    getattr(g, website + '_cookies').set(cookie_name,json.dumps(new_cookie))

    return cookies


@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    """
    添加用户, 访问地址如 /weibo/add/user/password
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return: 
    """
    g = get_conn()
    print(username, password)
    getattr(g, website + '_accounts').set(username, password)
    return json.dumps({'status': '1'})


@app.route('/<website>/count')
def count(website):
    """
    获取Cookies总数
    """
    g = get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
