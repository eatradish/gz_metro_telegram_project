import json
import requests
import logging
import metro_list
from dateutil.parser import parse

def cal_time(time, time2):
    time2 = int(time2)
    p_time = parse(time)
    time_hour = p_time.hour
    time_minute = p_time.minute
    time_minute = time_minute - time2
    if time_minute < 0:
        time_minute = 60 + time_minute
        time_hour = time_hour - 1
        if time_hour < 0:
            time_hour = 24 + time_hour
        time = repr(time_hour) + ":" + repr(time_minute)
        cal_time(time, time2)
    else:
        time = repr(time_hour)+ ":" + repr(time_minute)
    return time
def get_lineId(lineName):
    d = {"一号线": "1", "二号线": "2", "三号线": "3", "三北线": "3zx", "四号线": "4", "五号线": "5", "六号线": "6", "七号线": "7", "八号线": "8", "广佛线": "gf", "APM": "APM"}
    if lineName in d.keys():
        return d[lineName]
    else:
        return
def get_metro(startStation, endStation):
    url = 'http://cs.gzmtr.com/base/doSearchPathLine.do?callback=jQuery18008559129836403419_1506405972423'
    data = {'startStation': startStation, 'endStation': endStation}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    r = requests.post(url, data = data) #headers = headers)
    msg = r.text[41:-1]
    msg_list = []
    try:
        msg = json.loads(msg)
        s_info = '最佳乘车方案，途径 ' + repr(msg['count']) + ' 站，乘车时间 ' + msg['spendTime'] +' 分钟，票价 ' + repr(msg['price']) + ' 元'
        msg_list.append(s_info)
        for i in range(len(msg['lines'])):
            try:
                msg_list.append('从' + msg['lines'][i]['stationName'] + '出发，乘坐' + msg['lines'][i]['lineName'] + '到达' + msg['lines'][i + 1]['stationName'])
            except:
                continue
        lineId = get_lineId(msg['lines'][-2]['lineName'])
        t_url = 'http://cs.gzmtr.com/clkweb/doTimeService.do?callback=jQuery18009535422444381279_1506495968193&lineId=' + lineId
        t_r = requests.post(t_url)
        t = t_r.text[41:-1]
        time_msg = json.loads(t)
        time = 0
        for i in range(len(time_msg['list'])):
            if time_msg['list'][i]['stop'] == msg['lines'][-2]['stationName']:
                for j in range(len(time_msg['list'])):
                    if time_msg['list'][j]['stop'] == msg['lines'][-1]['stationName']:
                        if j > i:
                            time = time_msg['list'][j]['endTow']
                            if time == '—':
                                time = '不确定'
                        elif j < i:
                            time = time_msg['list'][j]['endOne']
                            if time == '—':
                                time = '不确定'
                        else:
                            pass
                    else:
                        pass
            else:
                pass
        try:
            time = cal_time(time, msg['spendTime'])
        except:
            time = '不确定'
        msg_list.append("理论最晚搭乘时间是: " + time)

    except:
        msg_list.append('找不到「' + startStation + '」或者「' + endStation + '」站点')
        lst = metro_list.get_list()
        for i in lst:
            import itertools as it
            c = ''.join(el[0] for el in it.takewhile(lambda t: t[0] == t[1], zip(i, startStation)))
            if c != '':
                for j in lst:
                    d = ''.join(el[0] for el in it.takewhile(lambda t: t[0] == t[1], zip(j, endStation)))
                    if d != '':
                        msg_list.append(i + ' ' + j)
        if len(msg_list) != 1:
            msg_lst2 = []
            msg_lst2.append('以下列出所有你可能要找的路线:')
            list3 = [msg_list[0], msg_lst2[0]]
            msg_list = list3 + msg_list[1:]
        else:
            msg_list.append('一个站名都没法好好输入你还是别坐地铁了')
    finally:
        msg = '\n'.join(msg_list)
    return msg