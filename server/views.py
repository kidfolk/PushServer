# Create your views here.
# coding=utf-8
import datetime
import httplib
import urllib
import json

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

token_filename = 'token.json'
group_filename = 'group.txt'


def index(request):
    print 'hello'
    if token_need_refresh():
        get_access_token()
    now = datetime.datetime.now()
    t = get_template('index.html')
    return HttpResponse(t.render(Context({'current_date': now})))

# 发送推送通知
def sendAll(request):
    if need_create_group():
        create_group('test', 'test baidu push')

    gid = open(group_filename, 'r').readline()
    push_group_msg(gid, 'hello')
    pushmsg_to_user('hello from python')
    return HttpResponse('Hello World!')


# 获取Access Token
def get_access_token():
    params = urllib.urlencode({'grant_type': 'client_credentials',
                               'client_id': 'OolSMsN2MoDL32EGongduzoY',
                               'client_secret': 'QuvQY04UxemBAagueV2GYnbnOHzIpzLc',
                               'response_type': 'code',
                               'redirect_uri': 'oob'})
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain'}

    conn = httplib.HTTPSConnection('openapi.baidu.com')
    conn.set_debuglevel(1)
    conn.request('POST', '/oauth/2.0/token', params, headers);

    response = conn.getresponse()
    json_obj = json.loads(response.read())
    json.dump(json_obj, open(token_filename, 'wb'))
    print 'access_token:', json_obj['access_token']
    print 'expires_in:', json_obj['expires_in']
    print 'refresh_token:', json_obj['refresh_token']
    print 'session_key:', json_obj['session_key']
    print 'session_secret:', json_obj['session_secret']


def create_group(name, info):
    token_data = json.load(open(token_filename, 'r'))
    params = urllib.urlencode({'method': 'create_group',
                               'access_token': token_data['access_token'],
                               'name': name,
                               'info': info})
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain'}

    conn = httplib.HTTPSConnection('channel.api.duapp.com')
    conn.set_debuglevel(1)
    conn.request('POST', '/rest/2.0/channel/channel', params, headers);

    response = conn.getresponse()
    json_obj = json.loads(response.read())
    gid = json_obj['response_params']['gid']
    group_file = open(group_filename, 'w+')
    group_file.write(gid)
    return gid

# 推送广播组消息
def push_group_msg(gid, msg):
    token_data = json.load(open(token_filename, 'r'))
    params = urllib.urlencode({'method': 'push_group_msg',
                               'access_token': token_data['access_token'],
                               'gid': gid,
                               'device_type': 3,
                               'messages': msg,
                               'msg_keys': msg})
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': '*/*',
               'Pragma': 'no-cache',
               'Host': 'channel.api.duapp.com',
               'User-Agent': 'curl/7.12.1'}

    conn = httplib.HTTPSConnection('channel.api.duapp.com')
    conn.set_debuglevel(1)
    conn.request('POST', '/rest/2.0/channel/channel', params, headers);

    response = conn.getresponse()
    print response.read()


def pushmsg_to_user(msg):
    token_data = json.load(open(token_filename, 'r'))
    params = urllib.urlencode({'method': 'pushmsg_to_user',
                               'access_token': token_data['access_token'],
                               'user_id': '1009554950909313206',
                               'device_type': 3,
                               'messages': msg,
                               'msg_keys': msg})
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': '*/*',
               'Pragma': 'no-cache',
               'Host': 'channel.api.duapp.com',
               'User-Agent': 'curl/7.12.1'}

    conn = httplib.HTTPSConnection('channel.api.duapp.com')
    conn.set_debuglevel(1)
    conn.request('POST', '/rest/2.0/channel/channel', params, headers);

    response = conn.getresponse()
    print response.read()


def token_need_refresh():
    token_data = None
    try:
        token_data = json.load(open(token_filename, 'r'))
    except IOError:
        print 'read token.json error'
    if token_data == None:
        return True
    return False


def need_create_group():
    group_id = None
    try:
        group_id = open(group_filename, 'r').readline()
    except IOError:
        print 'read group.txt error'

    if group_id == None:
        return True
    return False