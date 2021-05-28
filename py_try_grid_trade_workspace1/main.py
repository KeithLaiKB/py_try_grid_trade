# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import json
import time
from enum import Enum

import pytz as pytz
from pip._vendor import requests

from MyUrlTool import RequestMethod


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.





if __name__ == '__main__':
    print_hi('PyCharm')
    myurl='https://api.binance.com/api/v3/time'
    try:
        response = requests.request(RequestMethod.GET.value, url=myurl)
    except Exception as e:
        print(f"error: request to {myurl}, details:{e}")

    #
    if response.status_code == 200:
        result_content = response.json()
        #
        print(response)
        print(result_content)
        #
        long_time = result_content['serverTime']
        print(long_time)
        #
        #########################################################
        ################ 本机时间 ################
        # 需要除以1000, 并转化为当前时间
        timeArray = time.localtime(long_time / 1000)
        otherStyleTime = time.strftime("本机时间:%Y--%m--%d %H:%M:%S", timeArray)
        #
        print(timeArray)
        print(otherStyleTime)
        ################ UTC时间 ################
        str_utc_time        = datetime.datetime.utcfromtimestamp(long_time/1000)
        str_utc_time_format = datetime.datetime.strftime(str_utc_time, "UTC时间:%Y--%m--%d %H:%M:%S")
        #
        print(str_utc_time_format)
        ################ Toronto时间 ################
        current_timezone = pytz.timezone("America/Toronto")
        str_utc_time        = datetime.datetime.fromtimestamp(long_time / 1000, current_timezone)
        str_utc_time_format = datetime.datetime.strftime(str_utc_time, "Toronto时间:%Y--%m--%d %H:%M:%S")
        #
        print(str_utc_time_format)

    else:
        # do nothing
        print(response)
