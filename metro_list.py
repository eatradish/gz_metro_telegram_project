def get_list():
    with open('list.txt', 'rt') as f:
        data = f.read()
    lst = []
    num = 0
    for i in range(len(data)):
        if data[i] == ',':
            lst.append(data[num+2:i])
            num = i
    lst = list(set(lst))
    n = range(len(lst))
    for i in n:
        try:
            if ' ' in lst[i]:
                lst[i] = lst[i].replace(' ', '')
        except:
            continue
    return lst

if __name__ == '__main__':
    print(get_list())
