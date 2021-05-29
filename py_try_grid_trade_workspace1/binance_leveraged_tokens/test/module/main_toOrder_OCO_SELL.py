# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import time
from collections import OrderedDict

########################################################
import pytz
from pip._vendor import requests

from mytool.MyClient import MyClient
from MyUrlTool import RequestMethod

#myheaders = {"a": 'b'}
from mytool.MyTimeTool import MyTimeTool

myheaders = {}

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.








if __name__ == '__main__':
    print_hi('PyCharm')
    myurl = 'https://api.binance.com'
    myurl_resc_module = '/api/v3/order/oco'

    dict_myparam = {'symbol' : 'BTCUPUSDT', "side" : "SELL",
                    "quantity" : "0.31000000",
                    "price" : "72", "stopPrice" : "38", "stopLimitPrice" : "39",
                    "stopLimitTimeInForce":"GTC"}

    ########################获取 币安 servertime ###########################
    response = None
    try:
        myurl_servertime = 'https://api.binance.com/api/v3/time'
        response = requests.request(RequestMethod.GET.value, url=myurl_servertime)
    except Exception as e:
        print(f"error: request to {myurl_servertime}, details:{e}")

    result_content = response.json()
    long_time = result_content['serverTime']
    #
    # 需要用 币安 的 servertime做为timestamp 进行提交
    dict_myparam['timestamp'] = str(long_time)
    #dict_myparam['timestamp'] = "1622223697519"
    ########################获取 杠杆代币 的赎回记录 ###########################
    myclient1=MyClient()

    response = None
    try:
        response = myclient1.myrequest(RequestMethod.POST.value,headers=myheaders, url=myurl+myurl_resc_module, dict_myparam=dict_myparam,needSign=True)
    except Exception as e:
        print(f"error: request to {myurl+myurl_resc_module}, details:{e}")

    #
    if response.status_code == 200:
        result_content = response.json()
        #
        print(response)
        print(result_content)
        #
        data = OrderedDict(result_content[0])
        first_ele = list(data.items())[1]
        #long_time = result_content['serverTime']
        print(first_ele)
    else:
        # do nothing
        print(response)
