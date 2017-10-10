def get_lineId(lineName):
    d = {"一号线": "1", "二号线": "2", "三号线": "3", "三北线": "3zx", "四号线": "4", "五号线": "5", "六号线": "6", "七号线": "7", "八号线": "8", "广佛线": "gf", "APM": "APM"}
    if lineName in d.keys():
        return d[lineName]
    else:
        return

