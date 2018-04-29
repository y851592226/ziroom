# coding: utf8

import os
import sys
import requests
from traceback import format_exc
from functools import wraps
CUR_PATH = os.path.dirname(os.path.abspath(__file__))

def try_times(times=3):

    def warpper1(f):

        @wraps(f)
        def warpper2(*args, **kwds):
            try_time = 0
            while try_time < times:
                try:
                    result = f(*args, **kwds)
                    break
                except:
                    try_time += 1
                    logger.error('func:%s args:%s kwds:%s except:%s',
                                 f.__name__, args, kwds, format_exc())
                    if try_time < times:
                        time.sleep(3)
                    else:
                        raise
            return result

        return warpper2

    return warpper1

def cached(f):
    @wraps(f)
    def _wraps(*args, **kwargs):
        url = args[1]
        filename = CUR_PATH + '/html/' + url.replace('/', '|')
        if os.path.exists(filename):
            print 'exists'
            with open(filename, 'r') as file:
                content = file.read()
        else:
            content = f(*args, **kwargs)
            with open(filename, 'w') as file:
                file.write(content)
        return content
    return _wraps

class SpiderBase(object):

    def __init__(self):
        self.headers = {'Referer': 'http://m.ziroom.com/BJ/search.html', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        self.timeout = 15

    def http_get(self, url, params=None):
        resp = requests.get(
            url,
            params=params,
            headers=self.headers,
            timeout=self.timeout,
            verify=False)
        return resp.content

    def http_post(self, url, data=None):
        resp = requests.post(
            url,
            data=data,
            params=params,
            headers=self.headers,
            timeout=self.timeout,
            verify=False)
        return resp