# coding:utf-8
import json
import threading
import urllib2
import cookielib
from random import randint
import re
from time import sleep, time

import MySQLdb
from BeautifulSoup import BeautifulSoup
from movie import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')

douban_sorturl = 'http://movie.douban.com/chart'
sort_apiurl = 'https://movie.douban.com/j/chart/top_list?type=*&interval_id=100%3A90&action=&start=*&limit=*'
user_agentlist = [{'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'NOKIA5700/ UCWEB7.0.2.37/28/999','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':' Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'},
                      {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999','Cookie':'viewed="10759635"; bid=JIo4pcRYNCc; _vwo_uuid_v2=DCD31497BDD56A4E468C8886CD27F485B|4ac6fd42202f6888705d8926cbe7280b; gr_user_id=c6eda976-5757-4bb4-b5f1-b5d54427c343; __yadk_uid=FwwmBj5eQXFEQElxu5WFVqGEZ4yA9aGR; ll="108304"; ap=1; ps=y; __utmc=30149280; _pk_id.100001.8cb4=42fcd5b82997b6c6.1532064721.1.1532064721.1532064721.; ue="13237105778@sina.cn"; __utma=30149280.874095482.1532070122.1532070122.1532074146.2; __utmb=30149280.0.10.1532074146; __utmz=30149280.1532074146.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; push_doumail_num=0; dbcl2="181469379:CHcEps1oSpk"; ck=lmtc'}]
def get_useragent():
    '''
    返回20个user-agent中随即一个
    :return:
    '''
    return user_agentlist[randint(0,19)]

def load_sortpage(url):
    '''
    请求页面的分类信息
    并存储
    每一个分类的url
    :param url:
    :return:
    '''
    #获得请求头部
    head = get_useragent()
    #构建请求
    req = urllib2.Request(url,headers=head)
    #发送请求 获得response
    res = urllib2.urlopen(req)
    #读出网页
    sort_page = res.read().replace('\n','')
    #将读出的网页转码为utf-8
    #sort_page = sort_page
    #href="/typerank?type_name=.*?&type=(\d+)&   href="/typerank?type_name=纪录片&type=1
    pattern = re.compile('href="/typerank\?type_name=(.*?)&type=(\d+?)&')
    result = pattern.findall(sort_page)

    for item in result:
        type  = type_info(int(item[1]),item[0])
        
        conn = MySQLdb.connect("localhost", "root", "123456", "doubanf", charset='utf8')
        cursor = conn.cursor()
        try:
            # 执行sql语句
            cursor.execute(type.insert().encode('utf-8'))
            # 提交到数据库执行
            conn.commit()

        except MySQLdb.MySQLError as e:
            # 发生错误时回滚
            print(e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    return result


def load_sortinfo(apiurl,type,start,limit):
    '''
    加载出改分类下所有电影的信息
    请求Api 爬出数据
    :param apiurl: api地址
    :param start: 从start开始
    :param limit: 每次请求limit条数据
    :return:
    '''
    #获得请求头部
    #替换url中的参数，顺序不能乱
    url = apiurl
    url  = url.replace('*',str(type),1)
    url = url.replace('*', str(start), 1)
    url = url.replace('*', str(limit), 1)
    print url
    head = get_useragent()
    #构建请求
    req = urllib2.Request(url,headers=head)
    res = None
    try:
        # 发送请求 获得response
        res = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print(e.read())
        print('error')
    #读取字符串
    result = res.read()
    #加载程json格式
    resultjson = json.loads(result)

    for item in resultjson:
        actors = ''
        for actor in item['actors']:
            #避免sql中包含'
            actor = actor.replace("'", '_')
            actors += actor + ','
        actors = actors[:-1]
        regions = ''
        for region in item['regions']:
            regions += region + ','
        regions = regions[:-1]
        #构造电影信息
        movinfo = movie_info(str(item['id']),item['title'],actors,regions,item['release_date'],item['cover_url'],float(item['score']),int(item['rating'][1]),long(item['vote_count']),item['url'])
        #构造电影在其类型中的排名
        mov_rank = movie_type(int(type),movinfo.movie_id,int(item['rank']))
        #创建数据库连接池
        conn = MySQLdb.connect("localhost", "root", "123456", "doubanf", charset='utf8')
        #避免连接断开
        conn.ping(True)
        
        cursor = conn.cursor()
        #测试打印的数据库语句
        sql = movinfo.insert().encode('utf-8')
        try:
            # 执行sql语句
            cursor.execute(movinfo.insert().encode('utf-8'))
            # 提交到数据库执行
            conn.commit()
            cursor.execute(mov_rank.insert().encode('utf-8'))
            conn.commit()
        except MySQLdb.MySQLError as e:
            # 发生错误时回滚
            print('电影信息存储失败'+movinfo.movie_id)
            print(sql)
            print(e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        
        load_moviepage(movinfo.url, movinfo)
        sleep(1)

    if len(resultjson)>0:
        start += limit
        sleep(2)
        load_sortinfo(apiurl,type,start,limit)
    else:
        pass

# def loop_sortrequest(resultList):
#     threadlist = []
#     dbconection = []
#     for item in resultList:
#         tempdb = MySQLdb.connect("localhost", "root", "123456", "doubanf", charset='utf8')
#         dbconection.append(tempdb)
#         th = threading.Thread(target=load_sortinfo,args=(sort_apiurl,item[1],0,20,tempdb))
#         th.start()
#         threadlist.append(th)
# 
#     for item in threadlist:
#         item.join()
#     for itemdb in dbconection:
#         itemdb.close()

def load_moviepage(url,movie):
    '''
    请求每个电影的详细页面
    获取热评和话题
    电影简介
    :param url:
    :param movie:
    :param db:
    :return:
    '''
    #获得请求头部
    print url
    head = get_useragent()
    #构建请求
    req = urllib2.Request(url,headers=head)
    res = None
    try:
        #发送请求 获得response
        res = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        #print e.read()
        return
    #读出网页
    moviepage = res.read()
    #构建bs4
    soup = BeautifulSoup(moviepage)

    #如果简介需要展开
    #爬取需要展开的简介内容
    Allsynopsis = soup.findAll("span", "all hidden")
    if len(Allsynopsis) == 0:
        synopsis = soup.findAll(attrs={"property": "v:summary"})
        if len(synopsis) >0:
            movie.synopsis = synopsis[0].text.replace("'",'_')
            conn = MySQLdb.connect("localhost", "root", "123456", "doubanf", charset='utf8')
            conn.ping(True)
            cursor = conn.cursor()
            try:
                # 执行sql语句
                cursor.execute(movie.update_synopsis().encode('utf-8'))
                # 提交到数据库执行
                conn.commit()
            except MySQLdb.MySQLError as e:
                print('电影简介更新失败'+movie.movie_id)
                print(e)
                # 发生错误时回滚
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
        else:
            with open('error'+'.txt','w') as f:
                f.write(moviepage)
    else:
        movie.synopsis = Allsynopsis[0].text.replace("'",'_')
        conn = MySQLdb.connect("localhost", "root", "123456", "doubanf", charset='utf8')
        conn.ping(True)
        cursor = conn.cursor()
        try:
            # 执行sql语句
            cursor.execute(movie.update_synopsis().encode('utf-8'))
            # 提交到数据库执行
            conn.commit()
        except MySQLdb.MySQLError as e:
            print('电影简介更新失败'+movie.movie_id)
            print(e)
            # 发生错误时回滚
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    #https://movie.douban.com/j/review/id/full 热评api
    comments = soup.findAll("div","main review-item")
    #加载热评并存进数据库
    for com in comments:
        load_hotcomment('https://movie.douban.com/j/review/id/full',com.get('id'),movie.movie_id)

def load_hotcomment(url,commentid,movie_id):

    url = url.replace('id',commentid)
    # 获得请求头部
    head = get_useragent()
    # 构建请求
    req = urllib2.Request(url, headers=head)
    res = None
    try:
        # 发送请求 获得response
        res = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print e.read()
        return
    #将读取到的字符串转换为json数据格式
    resultjson = json.loads(res.read())
    #构造热评
    hot_com = hot_comment(long(commentid),resultjson['html'].replace('\'','_'),int(resultjson['votes']['totalcount']),int(resultjson['votes']['usecount']),int(resultjson['votes']['useless_count']),movie_id)
    conn = MySQLdb.connect("localhost", "root", "123456", "doubanf", charset='utf8')
    conn.ping(True)
    cursor = conn.cursor()
    try:
        # 执行sql语句
        cursor.execute(hot_com.insert().encode('utf-8'))
        # 提交到数据库执行
        conn.commit()
    except MySQLdb.MySQLError as e:
        print('热评存储失败'+str(hot_comment.comment_id))
        print(e)
        # 发生错误时回滚
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    result = load_sortpage(douban_sorturl)
    thlist = []

    for type in result:
        th = threading.Thread(target=load_sortinfo,args=(sort_apiurl,type[1],0,10,))
        th.start()
        sleep(2)
     
    # for x in thlist:
    #     x.join()
    #loop_sortrequest()
