def getDisctionaryOfLists(list):
    dict = {}
    for d in list:
        for key, value in d.items():
            if dict.get(key):
                dict[key].append(value)
            else:
                dict[key] = [value]
    return dict


def concatenateLists(list1, list2, separator):
    newList = []
    for i in range(len(list1)):
        newList.append("%s%s%s" % (list1[i], separator, list2[i]))
    return newList
