# coding: utf-8
import urllib
import urllib2
import re
import sys
import difflib
import json
from datetime import datetime
import random
import time,sched,os
import httplib
from threading import Timer
#from multiprocessing import Pool as ThreadPool
from multiprocessing.dummy import Pool as ThreadPool
import  signal
import lxml.etree as etree
#pool = ThreadPool(processes=2)


def getPoint(ykid): #送出多少，收到多少
    global proxies,agents
    index_url = r"http://120.55.238.158/api/statistic/inout?uid=251464826&id=" + ykid
    try_num = 0
    max_num = 100
#    request = urllib2.Request(index_url)
#    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586')
    while True:
        try:
            random_proxy = random.choice(proxies)
            proxy_support = urllib2.ProxyHandler({"http":random_proxy})
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)
            random_agent = random.choice(agents)
            request = urllib2.Request(index_url)
            request.add_header('User-Agent',random_agent)
            page = urllib2.urlopen(request, data=None, timeout=10)
            text = page.read()    
            inx = re.findall("\"gold\": \d+", text)[0]
            outx = re.findall("\"point\": \d+", text)[0]
            return inx.split(':')[-1], outx.split(':')[-1]
        except Exception,e:
            try_num += 1
            if try_num >=  max_num + 1:
                return -1,-1
            if try_num >= max_num:
                getNewProxy()
            continue
#    print text
def getInfo(ykid):
    randomid = random.randint(100000, 251464826)
    index_url = r"http://120.55.238.158/api/user/info?uid="+str(randomid)+"&id=" + ykid
    request = urllib2.Request(index_url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586')
    
    while True:
        try:
            page = urllib2.urlopen(request, data = None, timeout = 10)
            text = page.read()
            break
        except Exception,e:
            continue
    userinfo = json.loads(text)
    return text 

def getFans(ykid):
    global proxies,agents
    index_url = r"http://120.55.238.158/api/user/relation/numrelations?uid=251464826&id=" + ykid
    try_num = 0
    max_num = 100
    while True:
        try:
            random_proxy = random.choice(proxies)
            proxy_support = urllib2.ProxyHandler({"http":random_proxy})  
            opener = urllib2.build_opener(proxy_support)  
            urllib2.install_opener(opener)
            random_agent = random.choice(agents)
            request = urllib2.Request(index_url)
            request.add_header('User-Agent', random_agent)
            page = urllib2.urlopen(request, data=None, timeout=10)
            text = page.read()    
            inx = re.findall("\"num_followers\":\d+", text)[0]
            outx = re.findall("\"num_followings\":\d+", text)[0]
            return inx.split(':')[-1], outx.split(':')[-1]
        except Exception,e:
            try_num += 1
            if try_num >= max_num +1:
                return -1,-1
            if try_num >= max_num:
                getNewProxy()
            continue
#    print text

def getBoard(ykid):
    id_jsoninfo = dict()
    id_jsoninfo['count'] = "20"
    id_jsoninfo['id'] = ykid
    id_jsoninfo['request_id'] = "251464826"
    start = 0
    contri_list = []
    id_list = []
    
    while True:
        id_jsoninfo['start'] = start
        index_url = r"http://service.inke.com/api/day_bill_board/board?"
        while True:
            try:
                req = urllib2.Request(index_url)
                req.add_header('Content-Type', 'application/json')
                
                page = urllib2.urlopen(req, json.dumps(id_jsoninfo), timeout=10)

                text = page.read()
                break
            except Exception,e:
                continue

        if "\"count\":0" in text:
            break
        start += 20
        contri_list += re.findall("\"contribution\":\d+", text)
        id_list  += re.findall("\"id\":\d+", text)

    return [contri_list[i].split(":")[-1] + "\t" + id_list[i].split(":")[-1] for i in range(len(contri_list))]

def roomUser(roomid):
    print ""
    start = 0
    index_url = r"http://120.55.238.158/api/live/users?uid=251464826&count=20&id=" + roomid + "&start=" 
    rst = ""
    while True:

        while True:
            try:
                request = urllib2.Request(index_url + str(start))
                request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586')
                page = urllib2.urlopen(request, data=None, timeout=10)
                text = page.read()
                break
            except Exception,e:
                continue
        if "emotion" not in text:
            break
        rst += text

        start += 20
    return rst


def onlineUser(roomid):
    index_url = r"http://120.55.238.158/api/live/info?uid=251464826&id=" + roomid
    try_num = 0
    max_num = 100
    while True:
        try:
            random_proxy = random.choice(proxies)
            proxy_support = urllib2.ProxyHandler({"http":random_proxy})  
            opener = urllib2.build_opener(proxy_support)  
            urllib2.install_opener(opener)
 
            random_agent = random.choice(agents)
            request = urllib2.Request(index_url)
            request.add_header('User-Agent', random_agent)
            page = urllib2.urlopen(request, data=None, timeout=10)
            text = page.read()
            break
        except Exception,e:
            try_num += 1
            if try_num > max_num + 1:
                return -1
            if try_num > max_num:
                getNewProxy()
            continue
    #print text
    inx = re.findall("\"online_users\": \d+", text)[0]
#    print inx
    return inx.split(" ")[-1]   

proxies=["10.144.90.190:3128","10.142.42.177:3128","10.134.97.150:3128",
        "10.134.79.130:3128","10.134.62.238:3128","gpu.xiaoe.nm.ted:3128",
        "61.176.215.34:8080","220.194.213.52:8080","183.131.215.86:8080","60.169.19.66:9000","123.125.212.171:8080","61.176.215.7:8080","61.160.190.34:8888","171.8.79.91:8080",
        "218.60.55.3:8080","1.28.246.144:8080"]
#        "183.166.167.191:8080","220.194.213.52:8080" ,"61.130.97.212:8099","60.169.19.66:9000","115.231.128.81:8080"]
#    "60.169.19.66:9000","171.8.79.91:8080","115.231.128.79:8080","1.82.132.75:8080","171.8.79.143:8080"]
#    "111.8.22.215:8080","111.23.10.43:8080","111.23.10.27:8080","111.23.10.56:80","111.23.10.34:80","111.23.10.112:8080","111.23.10.174:8080","111.23.10.99:80","111.23.10.123:80",
#    "111.23.10.98:80","111.23.10.170:8080","111.23.10.12:80","111.23.10.175:8080","111.23.10.24:80","111.8.22.206:8080","111.23.10.173:80"]
agents =["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER","Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0"]
 

def nowPublish(ykid):
    index_url = r"http://service.inke.com/api/live/now_publish?cv=IK3.7.20_Android&uid=251464826&id=" + ykid 
    max_num = 100
    num = 0
    random_proxy = ''
    global proxies,agents
    while True:
        try:
            random_proxy = random.choice(proxies)
            proxy_support = urllib2.ProxyHandler({"http":random_proxy})  
            opener = urllib2.build_opener(proxy_support)  
            urllib2.install_opener(opener)
 
            random_agent = random.choice(agents)
            request = urllib2.Request(index_url)
            request.add_header('User-Agent', random_agent)
            page = urllib2.urlopen(request, data=None, timeout=10)
            text = page.read()
            if "live" in text:
                return text
            else:
                return 0
        except Exception,e:
            num += 1
#            print random_proxy
            if num >= max_num +1:
                localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                with open('./audienceNum/'+ykid+'.txt', 'a') as outfile: 
                    outfile.write(localtime +'\tProxy is dead!\n')
                    outfile.flush()
                with open('./income/'+ykid+'.txt', 'a') as outfile:
                    outfile.write(localtime +'\tProxy is dead!\n')
                    outfile.flush()
                with open('./follow/'+ykid+'.txt', 'a') as outfile:
                    outfile.write(localtime +'\tProxy is dead!\n')
                    outfile.flush()
                return -1
            if num >= max_num:
                getNewProxy()
            continue

def simpleAll(ykid):
    index_url = r"http://120.55.238.158/api/live/simpleall" 
    while True:
        try:
            request = urllib2.Request(index_url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586')
            page = urllib2.urlopen(request, data=None, timeout=10)
            text = page.read()
            break
        except Exception,e:
            continue
    print text
    if "\"id\": " + ykid in text:
        print True
    else:
        print False

def goodVoice(ykid):
    index_url = r"http://service.inke.com/api/live/themesearch?uid=251464826&keyword=666ABA8214206E5B" 
    while True:
        try:
            request = urllib2.Request(index_url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586')
            page = urllib2.urlopen(request, data=None, timeout=5)
            text = page.read()
            break
        except Exception,e:
            continue
    print text
    if "\"id\": " + ykid in text:
        print True
    else:
        print False

def skill(ykid):
    index_url = r"http://service.inke.com/api/live/themesearch?uid=251464826&keyword=AFCC0BC263924F20" 
    while True:
        try:
            request = urllib2.Request(index_url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586')
            page = urllib2.urlopen(request, data=None, timeout=10)
            text = page.read()
            break
        except Exception,e:
            continue
    print text
    if "\"id\": " + ykid in text:
        print True
    else:
        print False


'''
#print getBoard("10491827")
ykid = "17309175"
ykid = "9028876"
ykid = "34133193"

getPoint(ykid)
getInfo(ykid)
getFans(ykid)
getBoard(ykid)
roomid = "1497274518391314"
#roomUser(roomid)

onlineUser(roomid)
print nowPublish(ykid)
simpleAll(ykid)
'''

#s = sched.scheduler(time.time,time.sleep)

# 检测是否直播
def isLive(mydelay,ykid,name,s):
    global roomid,ispub
    res = nowPublish(ykid)
    if res == -1:
        print ykid
    if res == 0:
        ispub = False
    else:
#        pattern = r'creator'
#        pattern = r',\"creator\":(.*?),\"id\":\"(.*?)\",'
        p = re.compile(r',\"creator\":(.*?),\"id\":\"(.*?)\",')
         #                 ,\"creator\":(.*?),\"id\":(.*?)\",
  #      p = re.compile('(creator)')
        m =  p.findall(res)
#        m = re.match(pattern,res)
        print m
#        data = json.loads(res)
#        roomid =  data['live']['id']

        if m:
            ispub = True
            roomid = m[0][1]
            with open('./file/ispub.txt', 'a') as outfile:
                # 格式化成2016-03-20 11:45:39形式
                localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                try:
                    outfile.write(localtime + '\t' + res + '\n')
                    outfile.flush()
                except Exception as e:
                    print e
                    print "isLive()\n"
    print ispub,roomid
    s.enter(mydelay,0,isLive,(mydelay,ykid,name,s))
    s.run()

# 直播时获得房间人数
def getOnlineUser(mydelay,name,s):
    global ispub,roomid
    if ispub:
        online = onlineUser(roomid)
        with open('./file/room_number.txt', 'a') as outfile:
                localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                try:
                    outfile.write(localtime + '\t' + online + '\n')
                    outfile.flush()
                except Exception as e:
                    print e
                    print "getOnlineUser()\n"
    s.enter(mydelay,0,getOnlineUser,(mydelay,name,s))
    s.run()


def mymain(mydelay=5):
    uid = ["406393807", "39657083", "631180", "332490251", "4898129", "46147663", "323285590", "262960", "64725155", "57096255"];
    performs = [isLive, getOnlineUser]
    mydelays = [60, 30]
    ykid = uid[0]
    for i in xrange(2):
        print 'processing:',i
        s = sched.scheduler(time.time,time.sleep)
        if i == 0:
            Timer(0, performs[i], (mydelays[i],ykid,i,s)).start()
        else:
            Timer(1, performs[i], (mydelays[i],i,s)).start()
 
def dummy_test(func):
    ykid = "5361379"
    s = sched.scheduler(time.time,time.sleep)
    if func.__name__ == "isLive":
        isLive(60,ykid,func.__name__,s)
    elif func.__name__ == "getOnlineUser":
        getOnlineUser(10,func.__name__,s)


def mymain2(mydelay=5):
    performs = [isLive, getOnlineUser]
    results2 = pool.map(dummy_test, performs)
    pool.close()  
    pool.join()


#Anchor

class AnchorInfo:
    def __init__(self,portrait,gender,nick,id,level,online_users,pos):
        self.portrait = portrait
        self.gender = gender
        self.nick = nick
        self.id = id
        self.level = level
        self.online_users = online_users
        self.pos = pos
#        self.users_vec.push_back(online_users)
#        self.pos_vec.push_back(pos)   #  0-199 为正常位置 -1为停播  250 为离开热榜

AnchorMap = {}

def getHotList():
    index_url = r"http://120.55.238.158/api/live/simpleall" 
    text = ''
    while True:
        try:
            random_proxy = random.choice(proxies)
            proxy_support = urllib2.ProxyHandler({"http":random_proxy})  
            opener = urllib2.build_opener(proxy_support)  
            urllib2.install_opener(opener)
            random_agent = random.choice(agents)
            request = urllib2.Request(index_url)
            request.add_header('User-Agent', random_agent)
            page = urllib2.urlopen(request, data=None, timeout=10)
            text = page.read()
            data = json.loads(text)
            if data['dm_error'] == 0:
                for i in xrange(len(data['lives'])):
                    creator = data['lives'][i]['creator']
                    online_users = data['lives'][i]['online_users']
                    ai = AnchorInfo(creator['portrait'],creator['gender'],creator['nick'],creator['id'],creator['level'],online_users,i)
                    if len(AnchorMap) > 2000:
                        if ai.id not in AnchorMap:
                            continue
                    else:
                        AnchorMap[ai.id] = ai
                        
                    with open('./hotlist/'+str(ai.id)+'.txt', 'a') as outfile:
                      # 格式化成2016-03-20 11:45:39形式
                        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        try:
                            outfile.write(localtime +'\t' + str(round) +'\t' + str(ai.pos) + '\t' + str(ai.online_users) + '\n')
                            outfile.flush()
                        except Exception as e:
                            print e
                            print "getHotlist"
# 
#                    print ai.nick,ai.id,ai.gender
            break
        except Exception,e:
            print e
            print 'getHotlist'
            continue
    print len(AnchorMap.keys()),time.time()
#    print AnchorMap.keys()

   
def checkHotList(delaytime,s):
    global round
    getHotList()
    round += 1
    s.enter(delaytime,0,checkHotList,(delaytime,s))
    s.run()

def checkHotList2():
    global round
    while True:
        getHotList()
        round += 1
        time.sleep(60)


def checkIslive(ykid):    
    ispub = False
    roomid = 0
    res = nowPublish(ykid)
    if res == -1:
        ispub = False
        print ykid,res
#    print ykid,res
    elif res == 0:
        ispub = False
    else:
        p = re.compile(r',\"creator\":(.*?),\"id\":\"(.*?)\",')
        m =  p.findall(res)
#        data = json.loads(res)
#        roomid =  data['live']['id']
        if m:
            ispub = True
            roomid = m[0][1]
            with open('./file/ispub.txt', 'a') as outfile:
                # 格式化成2016-03-20 11:45:39形式
                localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                try:
                    outfile.write(localtime + '\t' + res + '\n')
                    outfile.flush()
                except Exception as e:
                    print e
                    print "isLive()\n"
    return ispub,roomid




def checkAudienceNum(ispub,ykid,roomid):
    if ispub:
        online = onlineUser(roomid)
        with open('./audienceNum/'+ykid+'.txt', 'a') as outfile:
                localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                try:
                    outfile.write(localtime +'\t'+ str(round)+ '\t' + str(roomid) + '\t' +online + '\n')
                    outfile.flush()
                except Exception as e:
                    print e
                    print "in CheckAudienceNum()"

def checkFollowNum(ispub,ykid,roomid):
    if ispub:
        inx,outx = getFans(ykid)
        if inx > -2 and outx > -2:
            with open('./follow/'+ykid+'.txt', 'a') as outfile:
                localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                try:
                    outfile.write(localtime + '\t' + str(round) + '\t' + str(roomid) + '\t' + str(inx) + '\t' + str(outx) + '\n')
                    outfile.flush()
                except Exception as e:
                    print e
                    print "in CheckFollowNum()"

def checkIncome(ispub,ykid,roomid):
    if ispub:
        inx,outx = getPoint(ykid) 
        if inx >-2 and outx > -2:
            with open('./income/'+ykid+'.txt', 'a') as outfile:
                localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                try:
                    outfile.write(localtime + '\t' + str(round) + '\t' + str(roomid) + '\t' + str(inx) + '\t' + str(outx) + '\n')
                    outfile.flush()
                except Exception as e:
                    print e
                    print "in CheckIncome()"
                                                                                                                


def checkInfo(ykid):
    ispub,roomid = checkIslive(str(ykid))
    Timer(0,checkAudienceNum,(ispub,str(ykid),roomid)).start()
    Timer(0,checkFollowNum,(ispub,str(ykid),roomid)).start()
    Timer(0,checkIncome,(ispub,str(ykid),roomid)).start()
    
#    checkAudienceNum(ispub,str(ykid),roomid)
#    checkFollowNum(ispub,str(ykid),roomid)
#    checkIncome(ispub,str(ykid),roomid)




def updateProxyList():
    global proxies
#    index_url = r"http://dev.kuaidaili.com/api/getproxy/?orderid=929829142512515&num=200&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&sep=2" 
#    index_url = r"http://dev.kuaidaili.com/api/getproxy/?orderid=929829142512515&num=500&b_pcchrome=1&b_pcie=1&b_pcff=1&b_android=1&b_iphone=1&protocol=1&method=1&an_tr=1&an_an=1&an_ha=1&sp1=1&sp2=1&sep=2"
    index_url= r"http://dev.kuaidaili.com/api/getproxy/?orderid=929829142512515&num=200&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&sp1=1&sp2=1&sep=2"
    text = ''
    proxies = []
    while True:
        try:
            request = urllib2.Request(index_url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586')
            page = urllib2.urlopen(request, data=None, timeout=10)
            text = page.read()
            proxies = text.split('\n')
            proxies.append("gpu.xiaoe.nm.ted:3128")
            break
        except Exception,e:
            print e
            continue
    print 'Proxy list is update!'
#    s.enter(delay,0,updateProxyList,(delay,s))

    


def checkAnchorInfo(delaytime,s):
    global AnchorMap,round
    use_proxy = 0
    print 'checkInfo[starting...]',time.time()
    if len(AnchorMap) > 0:
        getNewProxy()
#        for idx,uid in enumerate(AnchorMap.keys()):
 #           if (idx+1) % 30 == 0:
 #               use_proxy = 1 - use_proxy
 #               time.sleep(5)
#            checkInfo(uid)
        anchor_pool = ThreadPool(processes=20)#min(len(AnchorMap),2000))
        anchor_pool.map(checkInfo,AnchorMap.keys())
        anchor_pool.close()
        anchor_pool.join()
    print 'checkInfo[end...]',time.time()
    s.enter(delaytime,0,checkAnchorInfo,(delaytime,s))

def checkAnchorInfo2():
    global AnchorMap,round
    num = 0
    max_num = 5
    getNewProxy()
    print 'checkInfo[starting...]',time.time()
    if len(AnchorMap) > 0:
        while num < max_num:
            try:
                anchor_pool = ThreadPool(processes=200)#min(len(AnchorMap),500))
                anchor_pool.map(checkInfo,AnchorMap.keys())
                anchor_pool.close()
                anchor_pool.join()
                break
            except Exception,e:
                print 'CheckAnchorInfo Error!',e
                num += 1
                if num < max_num:
                    continue
                else:
                    print 'over!'
                    sys.exit(1)
    print 'checkInfo[end...]',time.time()


def getNewProxy():
    global proxies
    proxies = []
    proxies=["10.144.90.190:3128","10.142.42.177:3128","10.134.97.150:3128","10.134.79.130:3128","10.134.62.238:3128","gpu.xiaoe.nm.ted:3128"]
    num =0
    max_num = 10
    while num < max_num:
        try:
            random_proxy = random.choice(proxies)
            proxy_url = 'http://cn-proxy.com/'
            proxy_support = urllib2.ProxyHandler({"http":"gpu.xiaoe.nm.ted:3128"})
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)
            random_agent = random.choice(agents)
            request = urllib2.Request(proxy_url)
            request.add_header('User-Agent',random_agent)
            f = urllib2.urlopen(request, data=None, timeout=10)
            html = f.read()
            doc = etree.HTML(html.decode('utf-8'))
            proxy_set =doc.xpath("//tbody/tr")
            for row in proxy_set:
                ip = row.xpath(".//td[1]")
                port = row.xpath(".//td[2]")
                for tmp in zip(ip,port):
                    proxies.append(tmp[0].text+":"+tmp[1].text)
            break
        except Exception,e:
            num += 1
            print e
    print 'Proxy update done!'

def momo():
#    sched_hotlist = sched.scheduler(time.time,time.sleep)
#    Timer(0,checkHotList,(60,sched_hotlist)).start()
    Timer(0,checkHotList2).start()

    time.sleep(2)
    while True:
        checkAnchorInfo2()
        time.sleep(60)

#    sched_check = sched.scheduler(time.time,time.sleep)
#    sched_check.enter(2,0,checkAnchorInfo,(60,sched_check))
#    sched_check.run()


round = 0


if __name__ == "__main__":
#    mymain()
#    mymain2()
    momo()
#    getNewProxy()
