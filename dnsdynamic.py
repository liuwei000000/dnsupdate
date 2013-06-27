#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib,time
import urllib2, cookielib
import os
def get_wlan_ip():
  return urllib.urlopen("http://myip.dnsdynamic.org/").read()

def login(username, password):
  url = r'http://dcp.xinnet.com/Modules/agent/domain/domain_manage.jsp'
  image_url = r'http://dcp.xinnet.com/Modules/agent/domain/validate_picture.jsp'
  post_url = r'http://dcp.xinnet.com/domainLogin.do?method=domainEnter'
  post_url2 = r'http://www.xinnet.com/domainLogin.do'
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler)
  urllib2.install_opener(opener)
  urllib2.urlopen(url).read()

  print 'Login ...'

  outfile=open(r'/tmp/code.jpg', 'wd')
  outfile.write(opener.open(urllib2.Request(image_url)).read())
  outfile.close()

  os.system("tesseract /tmp/code.jpg -psm 7 out")
  code = open("out.txt").read(4)
  values={'domainName':username, 'password':password, 'checkCode':code}
  data=urllib.urlencode(values)
  urlcontent= opener.open(urllib2.Request(post_url, data)).read()
  if (urlcontent.find(r'验证码错误') > 0):
    print '登陆失败!!!'
    return None
  else:
    print '登陆成功!'
    values={'domainName':username, 'password':password, 'charset':'utf-8', 'method': 'doDomainLogin'}
    data=urllib.urlencode(values)
    content = opener.open(urllib2.Request(post_url2, data)).read()

    values={'domain': username, 'method':'domainDNS' }
    data=urllib.urlencode(values)
    request = urllib2.Request(post_url2, data)
    request.add_header('Referer', "http://www.xinnet.com/domainLogin.do")
    content = opener.open(request)
    print content.read()
    return content

def modify(ip, username, password):
  opener = login(username, password)
  if (opener == None) :
    return None

'''
  values={'method':'domainDNS', 'domain': username}
  data=urllib.urlencode(values)
  content = opener.open(urllib2.Request(post_url, data)).read()

  print content
  '''


