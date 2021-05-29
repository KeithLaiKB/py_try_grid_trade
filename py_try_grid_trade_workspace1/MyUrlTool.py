from enum import Enum


class RequestMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'



class MyUrlTool(object):
    def __init__(self, url=None):
        print("tool initiated")


    def convertDictToUrlParameter(myparams: dict):
        str_tmp = None
        #
        if bool(myparams) == False:
            print("do noting in convertDictToUrlParameter")
            str_tmp = ""
        elif bool(myparams) == True:
            str_tmp = ""
            #
            keys = list(myparams.keys())
            keys.sort()
            for (i, key) in zip(range(0, len(keys), 1), keys):
                #print(key)
                # 根据key获取value值
                value = myparams[key]
                #print(key, value)
                #
                if i == 0:
                    str_tmp = "" + key + "=" + value
                elif i >= 0:
                    str_tmp = str_tmp + "&" + key + "=" + value
            print("parameter in convertDictToUrlParameter:", str_tmp)
            # 以 f开头表示在字符串内支持大括号内的python 表达式
            # str_tmp = '&'.join([f"{key}={params[key]}" for key in params.keys()])
        return str_tmp