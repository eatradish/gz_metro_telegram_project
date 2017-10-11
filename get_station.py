import requests
import json
import pprint

def get_station(msg):
    url = 'http://cs.gzmtr.com/base/doSearchEntryAndResource.do?callback=jQuery18006481749776712236_1507753027311'
    data = {'station': msg}
    try:
        r = requests.post(url, data = data)
        j = json.loads(r.text[41:-1])
        lst = []
        for i in range(len(j['entrys'])):
            s = j['entrys'][i]['entryname']
            lst.append(s)
            for k in range(len(j['entrys'][i]['resources'])):
                try:
                    lst[i] = lst[i] + '，' +j['entrys'][i]['resources'][k]['namecn']
                except:
                    continue
        msg = '\n'.join(lst)
    except:
        msg = '没有出口信息，用法: /search_station + 站点'
    return msg

