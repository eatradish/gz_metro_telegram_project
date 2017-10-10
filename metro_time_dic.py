import requests
import json
from get_lineId import get_lineId

def json_result(lineId):
    url = 'http://cs.gzmtr.com/clkweb/doTimeService.do?callback=jQuery18009535422444381279_1506495968193&lineId=' + lineId
    r = requests.post(url)
    j = json.loads(r.text[41:-1])
    return j

def format_result(json_result):
    msg_list = []
    msg_list.append('方向 / 首班车 // 尾班车')
    s = '车站 / ' + json_result['list'][0]['startOne'] + '方向 / ' + json_result['list'][0]['startTow'] + '方向 // ' + json_result['list'][0]['endOne'] + '方向 / ' + json_result['list'][0]['endTow'] + '方向'
    if 'endThree' in json_result['list'][0].keys():
        s = s + ' / ' + json_result['list'][0]['endThree'] + '方向'
    msg_list.append(s)
    for i in range(1, len(json_result['list'])):
        s2 = json_result['list'][i]['stop'] + ' ' + json_result['list'][i]['startOne'] + ' ' + json_result['list'][i]['startTow'] + ' ' + json_result['list'][i]['endOne'] + ' ' + json_result['list'][i]['endTow']
        if 'endThree' in json_result['list'][0].keys():
            s2 = s2 + ' ' + json_result['list'][i]['endThree']
        msg_list.append(s2)
    msg = '\n'.join(msg_list)
    return msg

def main():
    lineId = get_lineId('三北线')
    j = json_result(lineId)
    msg = format_result(j)
    print(msg)

if __name__ == '__main__':
    main()
