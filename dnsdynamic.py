#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib, urllib2, cookielib
import os
from time import sleep
from lxml import etree
import random

url = r'http://dcp.xinnet.com/Modules/agent/domain/domain_manage.jsp'
image_url = r'http://dcp.xinnet.com/Modules/agent/domain/validate_picture.jsp'
post_url = r'http://dcp.xinnet.com/domainLogin.do?method=domainEnter'
post_url2 = r'http://www.xinnet.com/domainLogin.do'
c_url = r'http://mydns3.xinnet.com/dwr/exec/validateAjaxManage.updateRecords.dwr'
AGAIN = 3

def write_ip(ip):
  try:
    rt = open("/tmp/last_ip.txt", 'w').write(ip)
  except:
    return

def read_ip():
  try:
    rt = open("/tmp/last_ip.txt").read()
  except:
    return ""
  return rt

def get_wlan_ip():
  return urllib2.urlopen("http://myip.dnsdynamic.org/").read()

class HTTPReferProcessor(urllib2.BaseHandler):
  def __init__(self):
    self.referer = None

  def http_request(self, request):
    request.add_unredirected_header("User-Agent", "Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0")
    if ((self.referer is not None) and \
        (not request.has_header("Referer"))):
        request.add_unredirected_header("Referer", self.referer)
        print "Referer:", self.referer
    return request

  def http_response(self, request, response):
    self.referer = response.geturl()
    return response

  http_request = http_request
  http_response = http_response

def m_self(username, password, again = 0):
  try:
    cip = get_wlan_ip()
    wip = cip
  except:
    print '读取本地ip出错'
    return None

  if len(cip.split('.')) != 4:
    print '读取本地ip出错'
    return None

  if ((cip == read_ip()) and \
      (random.randint(1, 40) != 4) and \
      (random.randint(1, 40) != 5)):
    print '和上次修改的ip相同'
    return

  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), HTTPReferProcessor)
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
    if (again < AGAIN ):
      print '登陆失败!', '重试:', str(again),
      sleep(1)
      print '...'
      return m_self(username, password, again + 1)
    else:
      return '登陆失败!重试失败'
  else:
    print '登陆成功!'

  values={'domainName':username, 'password':password, 'charset':'utf-8', 'method': 'doDomainLogin'}
  data=urllib.urlencode(values)
  content = opener.open(urllib2.Request(post_url2, data)).read()

  sleep(2)
  values={'domain': username, 'method':'domainDNS' }
  data=urllib.urlencode(values)
  request = urllib2.Request(post_url2, data)
  content = opener.open(request).read()

  node = etree.HTML(content).find(".//table[@id='tbca']//tr[2]/td[2]")
  if (node == None):
    if (again < AGAIN ):
      print '读取ip出错!', '重试:', str(again)
      sleep(2)
      print '...'
      return m_self(username, password, again + 1)
    else:
      print '读取ip出错, 重试失败'
      return None

  sip = "".join(node.text.split())
  if sip == cip :
    print '相同ip 不动作'
    write_ip(wip)
    return None

  print 'ip变化,修改ip'
  sleep(1)
  cip = "String:" + cip
  print cip
  values = {
          'callCount'    :'1',
          'c0-scriptName':'validateAjaxManage',
          'c0-methodName':'updateRecords',
          'c0-id'        : str(random.randint(1000,9999)) + "_" + str(int(time.time())) + str(random.randint(100,999)),
          'c0-param0'    :'string:A',
          'c0-param1'    :'string:www.iaskwho.com',
          'c0-param2'    : cip,
          'c0-param3'    :'string:124060884',
          'c0-param4'    :'number:3600',
          'c0-param5'    :'number:0',
          'c0-param6'    :'string:123.100.5.80',
          'c0-param7'    :'string:iaskwho.com',
          'c0-param8'    :'string:',
          'c0-param9'    : cip,
          'c0-param10'   :'string:null',
          'xml'          :'true'
          }

  data = urllib.urlencode(values)
  request = urllib2.Request(c_url, data)

  request.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
  request.add_header("Accept-Language", "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3")
  request.add_header("Content-Type","text/plain; charset=UTF-8")
  request.add_header("Accept-Encoding", "gzip, deflate")

  try:
    content = opener.open(request).read()
  except:
    print '修改失败'
    return None

  #做一个简单的判断是否修改成功
  if (len(content) > 200 or c.find("var s0=null") < 0):
    print '修改失败'
    return None

  print '修改成功: ', cip
  write_ip(wip)


if __name__ == '__main__':
  m_self('iaskwho.com', 'idle4443')
