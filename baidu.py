#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib, urllib2, cookielib
import os
import pickle
from time import sleep
from lxml import etree
import random

#url = r'http://openresearch.baidu.com/activityprogress.jhtml?channelId=577'
url = r'https://orsso.baidu.com/login?TARGET=http%3A%2F%2Fopenresearch.baidu.com%2Factivityprogress.jhtml%3FchannelId%3D577'
#url = r'http://openresearch.baidu.com/activityprogress.jhtml?channelId=577'

class SimpleCookieHandler(urllib2.BaseHandler):
  def http_request(self, req):
    simple_cookie = 'Hm_lvt_d9fd67e9091ec594840ed821a77e8c4e=1380186679,1380253348,1380264226,1380503351; BAIDUID=B565AA6371649D6DB5F5D39B9D8DC416:FG=1; BDUSS=WJWMVRCaTdvR3lmSE1jbTVMQXo0WUY0OFZNM1BLZXFIQ09FSWdlR1RMQ0RQbXRTQVFBQUFBJCQAAAAAAAAAAAEAAACX0pY4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIOxQ1KDsUNSc; bdshare_firstime=1380168038718; JSESSIONID=70D69226FD15C85D1A862368BCB10B08; clientlanguage=zh_CN; Hm_lpvt_d9fd67e9091ec594840ed821a77e8c4e=1380503351'
    if not req.has_header('Cookie'):
      req.add_unredirected_header('Cookie', simple_cookie)
    else:
      cookie = req.get_header('Cookie')
      #req.add_unredirected_header('Cookie', simple_cookie + '; ' + cookie)
    print req.headers
    return req

def check():
  print 'Load ...'
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), SimpleCookieHandler())
  urllib2.install_opener(opener)
  content = urllib2.urlopen(url).read()
  print 'Load OK'

  sort = pickle.load(open("/tmp/baidu.txt", 'rb'))
  for i in ['2', '3', '4', '5', '6', '7']:
    name = ( (etree.HTML(content).xpath(".//div[@class='hd_zilt']/div[2]//tr["+ i + "]/td[2]/text()")[0]).strip())
    f = ( float((etree.HTML(content).xpath(".//div[@class='hd_zilt']/div[2]//tr["+ i + "]/td[3]/text()")[0]).strip()) )
    if (sort.has_key(name)):
        if (sort[name] < f):
          sort[name] = f
    else:
      sort[name] = f;
  print sort
  pickle.dump(sort, open("/tmp/baidu.txt", 'w'))

if __name__ == '__main__':
  check()
