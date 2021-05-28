import datetime
import time

import pytz
from numpy.core import long


class MyTimeTool:
    @staticmethod
    def convertTimestampToLocaltime(timestamp, format=None):
        timeArray_temp = time.localtime(timestamp / 1000)
        if format == None:
            format = "%Y--%m--%d %H:%M:%S"
            otherStyleTime = time.strftime(format, timeArray_temp)
        elif format != None:
            otherStyleTime = time.strftime(format, timeArray_temp)
        #
        print(timeArray_temp)
        print(otherStyleTime)
        return otherStyleTime

    @staticmethod
    def convertTimestampToUtctime(timestamp, format=None):
        str_time_temp = datetime.datetime.utcfromtimestamp(timestamp/1000)
        if format == None:
            format = "%Y--%m--%d %H:%M:%S"
            otherStyleTime = datetime.datetime.strftime(str_time_temp, format)
        elif format != None:
            otherStyleTime = datetime.datetime.strftime(str_time_temp, format)
        #
        print(str_time_temp)
        print(otherStyleTime)
        return otherStyleTime

    @staticmethod
    def convertTimestampToSpecifictime(timestamp, timezone, format=None):
        current_timezone = pytz.timezone(timezone)
        str_specific_time_temp = datetime.datetime.fromtimestamp(timestamp / 1000, current_timezone)
        if format == None:
            format = "%Y--%m--%d %H:%M:%S"
            str_specific_time_format_tmp = datetime.datetime.strftime(str_specific_time_temp, format)
        elif format != None:
            str_specific_time_format_tmp = datetime.datetime.strftime(str_specific_time_temp, format)
        #
        print(str_specific_time_temp)
        print(str_specific_time_format_tmp)
        return str_specific_time_format_tmp

    # str_time: '2021-05-28_04:30:00'
    # str_tz  : 'America/Toronto'
    # format  : '%Y-%m-%d_%H:%M:%S'
    @staticmethod
    def convertSpecifictimeToTimestamp(str_time, str_tz, format=None):
        ###############################
        # 方法一
        # origin -> timestamp
        #
        # step1: 转换成 datetime格式
        # dt_orig = datetime.datetime.strptime(str_time, format)
        # step2: 设定指定timezone
        # tz_orig = pytz.timezone(str_tz)
        # step3: 获得指定timezone的时间
        # lclz_time_orig = tz_orig.localize(dt_orig, is_dst=False)
        # step4:  然后 timestamp()
        # long_time = lclz_time_orig.timestamp()
        ###############################
        # 方法二
        # origin -> utc -> timestamp
        #
        # step1: 转换成 datetime格式
        dt_orig = datetime.datetime.strptime(str_time, format)
        # step2: 设定指定timezone
        tz_orig = pytz.timezone(str_tz)
        # step3: 获得指定timezone的时间
        lclz_time_orig = tz_orig.localize(dt_orig, is_dst=False)
        # step4:  设定utc的timezone
        tz_utc = pytz.UTC
        # step5:  获得utc timezone的时间
        dt_utc = lclz_time_orig.astimezone(tz_utc)
        # step6:  然后 timestamp()
        long_time = dt_utc.timestamp()

        #############################
        ### 验证
        # 因为我们是 origin 转换成 utc
        # 为了验证 我们就去看看
        # utc 转换成 origin_after  是否等于     原始的 origin
        #
        # utc_timestamp -> datetime_utc
        str_utc_test = MyTimeTool.convertTimestampToSpecifictime(long_time * 1000, "utc", format)
        dt_utc_test = datetime.datetime.strptime(str_utc_test, format)
        # datetime_utc ->  origin_after
        origin_after = dt_utc_test.replace(tzinfo=pytz.utc).astimezone(tz_orig)
        print(lclz_time_orig)
        print(origin_after)
        if lclz_time_orig == origin_after:
            print("验证成功:", lclz_time_orig, origin_after)
        if lclz_time_orig.timestamp()== long_time:
            print("验证成功:", lclz_time_orig.timestamp(), long_time)

        long_time = long_time*1000
        return long_time
