import json
import os
from collections import OrderedDict

from pip._vendor import requests

from MyDealFile import MyDealFile
from MyUrlTool import RequestMethod
from mytool.MyClient import MyClient
from mytool.MyTimeTool import MyTimeTool


class OcoManagement:



    '''
    [
        {
            "orderListId":32802265,
            "contingencyType":"OCO",
            "listStatusType":"EXEC_STARTED",
            "listOrderStatus":"EXECUTING",
            "listClientOrderId":"GYZswuMhs88Yv1Z0Hpynkw",
            "transactionTime":1622266478723,
            "symbol":"BTCUPUSDT",
            "orders":[
                {
                    "symbol":"BTCUPUSDT",
                    "orderId":170393702,
                    "clientOrderId":"8knuqaehpVTAnvP1Nrnwzh"
                },
                {
                    "symbol":"BTCUPUSDT",
                    "orderId":170393703,
                    "clientOrderId":"AuEx7CkxWjQ3BOTefR1pwt"
                }
            ]
        }
    ]
    '''
    @staticmethod
    def getNowAllOcoList():
        myurl = 'https://api.binance.com'
        myurl_resc_module = '/api/v3/openOrderList'
        #
        dict_myparam = {}
        myheaders = {}
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
        # dict_myparam['timestamp'] = "1622223697519"
        ########################获取 当前挂单 ###########################
        myclient1 = MyClient()

        response = None
        try:
            response = myclient1.myrequest(RequestMethod.GET.value, headers=myheaders, url=myurl + myurl_resc_module,
                                           dict_myparam=dict_myparam, needSign=True)
        except Exception as e:
            print(f"error: request to {myurl + myurl_resc_module}, details:{e}")

        #
        if response.status_code == 200:
            result_content = response.json()
            #
            print(response)
            print(result_content)
            #
            #data = OrderedDict(result_content[0])
            #first_ele = list(data.items())[1]
            # long_time = result_content['serverTime']
            #first_ele = list(data.items())[1]
            #print(first_ele)
            '''
            for listtmp in result_content:
                if listtmp["symbol"] == "BTCUPUSDT":
                    print("orderListId is:",listtmp["orderListId"])
            '''
            return result_content
        else:
            # do nothing
            print(response)
            return None



    @staticmethod
    def getNowOcoListBySymbol(mysymbol):
        json_allOrderlist = OcoManagement.getNowAllOcoList()
        #
        result_orderListId = None
        #
        if json_allOrderlist is not None and json_allOrderlist !="":
            for listtmp in json_allOrderlist:
                #if listtmp["symbol"] == "BTCUPUSDT":
                if listtmp["symbol"] == mysymbol:
                    result_orderListId = listtmp["orderListId"]
                    print("orderListId is:",result_orderListId)
                    break

        return result_orderListId


    '''
    {
        "orderListId":32807349,
        "contingencyType":"OCO",
        "listStatusType":"EXEC_STARTED",
        "listOrderStatus":"EXECUTING",
        "listClientOrderId":"DC2NolQIAfYwjkYtLf3NQT",
        "transactionTime":1622271824434,
        "symbol":"BTCUPUSDT",
        "orders":[
            {
                "symbol":"BTCUPUSDT",
                "orderId":170428852,
                "clientOrderId":"7YxOrMLnGzKgO3whRgp91X"
            },
            {
                "symbol":"BTCUPUSDT",
                "orderId":170428853,
                "clientOrderId":"v9z773FPBWDInyrWwd3UNT"
            }
        ],
        "orderReports":[
            {
                "symbol":"BTCUPUSDT",
                "orderId":170428852,
                "orderListId":32807349,
                "clientOrderId":"7YxOrMLnGzKgO3whRgp91X",
                "transactTime":1622271824434,
                "price":"39.00000000",
                "origQty":"0.31000000",
                "executedQty":"0.00000000",
                "cummulativeQuoteQty":"0.00000000",
                "status":"NEW",
                "timeInForce":"GTC",
                "type":"STOP_LOSS_LIMIT",
                "side":"SELL",
                "stopPrice":"38.00000000"
            },
            {
                "symbol":"BTCUPUSDT",
                "orderId":170428853,
                "orderListId":32807349,
                "clientOrderId":"v9z773FPBWDInyrWwd3UNT",
                "transactTime":1622271824434,
                "price":"72.00000000",
                "origQty":"0.31000000",
                "executedQty":"0.00000000",
                "cummulativeQuoteQty":"0.00000000",
                "status":"NEW",
                "timeInForce":"GTC",
                "type":"LIMIT_MAKER",
                "side":"SELL"
            }
        ]
    }
    
    '''
    @staticmethod
    def placeAnOcoOder(dict_myparam):
        myurl = 'https://api.binance.com'
        myurl_resc_module = '/api/v3/order/oco'
        '''
        dict_myparam = {'symbol': 'BTCUPUSDT', "side": "SELL",
                        "quantity": "0.31000000",
                        "price": "72", "stopPrice": "38", "stopLimitPrice": "39",
                        "stopLimitTimeInForce": "GTC"}
        '''
        myheaders = {}
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
        # dict_myparam['timestamp'] = "1622223697519"
        ############################## 下OCO单 ##############################
        myclient1 = MyClient()
        response = None
        #
        try:
            response = myclient1.myrequest(RequestMethod.POST.value, headers=myheaders, url=myurl + myurl_resc_module,
                                           dict_myparam=dict_myparam, needSign=True)
        except Exception as e:
            print(f"error: request to {myurl + myurl_resc_module}, details:{e}")

        #
        if response.status_code == 200:
            result_content = response.json()
            #
            print(response)
            print(result_content)
            #
            ################################# save this transaction history json #################################
            ############ get root path  ###############
            my_project_name = 'py_try_grid_trade_workspace1'
            project_path = os.path.abspath(os.path.dirname(__file__))
            print(project_path)
            root_path = project_path[:project_path.find("{}\\".format(my_project_name)) + len("{}\\".format(my_project_name))]
            print('this project name：{}\r\nthis project root path：{}'.format(my_project_name, root_path))
            ############ create sub path ###############
            myTransactionTime = result_content['transactionTime']
            str_now_time_tmp = MyTimeTool.convertTimestampToLocaltime_str(myTransactionTime, "PlaceOco_%Y_%m_%d__%H_%M_%S")
            now_time_tmp = MyTimeTool.convertStrTimeToLocaltime_tm(str_now_time_tmp, "PlaceOco_%Y_%m_%d__%H_%M_%S")
            #
            # 例如
            # E:\mygit_workspace\grid_trade\py_try_grid_trade\py_try_grid_trade_workspace1\personal_myorder_record\placeorder\y_2021\m_05\d_29
            # PlaceOco_2021_05_29__03_48_12.json
            #
            ############ year ##########
            year_tmp = "y_" + str(now_time_tmp.tm_year)
            #
            ############ month ##########
            month_tmp = str(now_time_tmp.tm_mon)
            # 如果得到的是 5  那么 日子要弄成 m_05
            if len(month_tmp) == 1:
                month_tmp = "m_" +  "0" + month_tmp
            # 如果得到的是 12 那么 日子要弄成 m_12
            elif len(month_tmp) == 2:
                month_tmp = "m_" + month_tmp
            #
            ############ day #############
            day_tmp = str(now_time_tmp.tm_mday)
            # 如果得到的是 5  那么 日子要弄成 d_05
            if len(day_tmp) == 1:
                day_tmp = "d_" +  "0" + day_tmp
            # 如果得到的是 15 那么 日子要弄成 d_15
            elif len(day_tmp) == 2:
                day_tmp = "d_" + day_tmp
            #
            ########### mkdir ###########
            str_storePath = root_path + "\\personal_myorder_record" + "\\placeorder" + "\\" + year_tmp + "\\" + month_tmp + "\\"+ day_tmp
            MyDealFile.mymkdir(str_storePath)
            #
            ###### write json file #######
            filename = str_storePath + "\\" + str_now_time_tmp + ".json"
            with open(filename, 'w') as file_obj:
                json.dump(result_content, file_obj)

        else:
            # do nothing
            print(response)

    '''
    {
        "orderListId":32809724,
        "contingencyType":"OCO",
        "listStatusType":"ALL_DONE",
        "listOrderStatus":"ALL_DONE",
        "listClientOrderId":"wIs5f8ondmWSrRwhhQwQLZ",
        "transactionTime":1622275814681,
        "symbol":"BTCUPUSDT",
        "orders":[
            {
                "symbol":"BTCUPUSDT",
                "orderId":170451500,
                "clientOrderId":"dcWstc3qk23oNDrpdtE3KU"
            },
            {
                "symbol":"BTCUPUSDT",
                "orderId":170451501,
                "clientOrderId":"rFsQ2V2UAcSQinmuLvFdJh"
            }
        ],
        "orderReports":[
            {
                "symbol":"BTCUPUSDT",
                "origClientOrderId":"dcWstc3qk23oNDrpdtE3KU",
                "orderId":170451500,
                "orderListId":32809724,
                "clientOrderId":"CReYh6uLWnpXm5sHtwLJ8F",
                "price":"39.00000000",
                "origQty":"0.31000000",
                "executedQty":"0.00000000",
                "cummulativeQuoteQty":"0.00000000",
                "status":"CANCELED",
                "timeInForce":"GTC",
                "type":"STOP_LOSS_LIMIT",
                "side":"SELL",
                "stopPrice":"38.00000000"
            },
            {
                "symbol":"BTCUPUSDT",
                "origClientOrderId":"rFsQ2V2UAcSQinmuLvFdJh",
                "orderId":170451501,
                "orderListId":32809724,
                "clientOrderId":"CReYh6uLWnpXm5sHtwLJ8F",
                "price":"72.00000000",
                "origQty":"0.31000000",
                "executedQty":"0.00000000",
                "cummulativeQuoteQty":"0.00000000",
                "status":"CANCELED",
                "timeInForce":"GTC",
                "type":"LIMIT_MAKER",
                "side":"SELL"
            }
        ]
    }
    
    '''
    @staticmethod
    def deleteOcoOderListBySymbolAndOrderListId(mySymbol, myOrderListId):
        myurl = 'https://api.binance.com'
        myurl_resc_module = '/api/v3/orderList'

        #dict_myparam = {'symbol': 'BTCUPUSDT', "orderListId": "32802265"}
        dict_myparam = {'symbol': mySymbol, "orderListId": myOrderListId}
        myheaders = {}
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
        # dict_myparam['timestamp'] = "1622223697519"
        ############################## 删除OCO单 ##############################
        myclient1 = MyClient()

        response = None
        try:
            response = myclient1.myrequest(RequestMethod.DELETE.value, headers=myheaders, url=myurl + myurl_resc_module,
                                           dict_myparam=dict_myparam, needSign=True)
        except Exception as e:
            print(f"error: request to {myurl + myurl_resc_module}, details:{e}")

        #
        if response.status_code == 200:
            result_content = response.json()
            #
            print(response)
            print(result_content)
            #
            ################################# save this transaction history json #################################
            ############ get root path  ###############
            my_project_name = 'py_try_grid_trade_workspace1'
            project_path = os.path.abspath(os.path.dirname(__file__))
            print(project_path)
            root_path = project_path[
                        :project_path.find("{}\\".format(my_project_name)) + len("{}\\".format(my_project_name))]
            print('this project name：{}\r\nthis project root path：{}'.format(my_project_name, root_path))
            ############ create sub path ###############
            myTransactionTime = result_content['transactionTime']
            str_now_time_tmp = MyTimeTool.convertTimestampToLocaltime_str(myTransactionTime,
                                                                          "PlaceOco_%Y_%m_%d__%H_%M_%S")
            now_time_tmp = MyTimeTool.convertStrTimeToLocaltime_tm(str_now_time_tmp, "PlaceOco_%Y_%m_%d__%H_%M_%S")
            #
            # 例如
            # E:\mygit_workspace\grid_trade\py_try_grid_trade\py_try_grid_trade_workspace1\personal_myorder_record\placeorder\y_2021\m_05\d_29
            # PlaceOco_2021_05_29__03_48_12.json
            #
            ############ year ##########
            year_tmp = "y_" + str(now_time_tmp.tm_year)
            #
            ############ month ##########
            month_tmp = str(now_time_tmp.tm_mon)
            # 如果得到的是 5  那么 日子要弄成 m_05
            if len(month_tmp) == 1:
                month_tmp = "m_" + "0" + month_tmp
            # 如果得到的是 12 那么 日子要弄成 m_12
            elif len(month_tmp) == 2:
                month_tmp = "m_" + month_tmp
            #
            ############ day #############
            day_tmp = str(now_time_tmp.tm_mday)
            # 如果得到的是 5  那么 日子要弄成 d_05
            if len(day_tmp) == 1:
                day_tmp = "d_" + "0" + day_tmp
            # 如果得到的是 15 那么 日子要弄成 d_15
            elif len(day_tmp) == 2:
                day_tmp = "d_" + day_tmp
            #
            ########### mkdir ###########
            str_storePath = root_path + "\\personal_myorder_record" + "\\deleteorder" + "\\" + year_tmp + "\\" + month_tmp + "\\" + day_tmp
            MyDealFile.mymkdir(str_storePath)
            #
            ###### write json file #######
            filename = str_storePath + "\\" + str_now_time_tmp + ".json"
            with open(filename, 'w') as file_obj:
                json.dump(result_content, file_obj)

        else:
            # do nothing
            print(response)






