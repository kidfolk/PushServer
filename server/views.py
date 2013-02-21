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


def index(request):
    print 'hello'
    if token_need_refresh():
        get_access_token()
    now = datetime.datetime.now()
    t = get_template('index.html')
    return HttpResponse(t.render(Context({'current_date': now})))

# 发送推送通知
def sendAll(request):
    print 'sendAll'
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


def token_need_refresh():
    token_data = None
    try:
        token_data = json.load(open(token_filename, 'r'))
    except IOError:
        print 'read token.json error'
    if token_data == None:
        return True
    return False