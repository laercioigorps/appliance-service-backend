
def getDisctionaryOfLists(list):
    dict = {}
    for d in list:
        for key, value in d.items():
            if(dict.get(key)):
                dict[key].append(value)
            else:
                dict[key] = [value]
    return dict