import json
import time

from myoco.management.OcoManagement import OcoManagement
from normalcheck.main import print_hi

if __name__ == '__main__':
    print_hi('PyCharm')

    dict_myparam = {'symbol': 'BTCUPUSDT', "side": "BUY",
                    "quantity": "0.5",
                    "price": "20.000", "stopPrice": "100.000", "stopLimitPrice": "30.000",
                    "stopLimitTimeInForce": "GTC"}
    json_placeorder_result = OcoManagement.placeAnOcoOder(dict_myparam)
    print(json_placeorder_result["result"])
    print(json_placeorder_result["json_file_path"])
    print(json_placeorder_result["json_file_name_without_suffix"])
    #
    ###############################
    dict_operate_history = {"midprice": str(666)+"测试",
                            "price": "20.000", "stopPrice": "100.000", "stopLimitPrice": "30.000",
                            }
    filename = json_placeorder_result["json_file_path"] + "\\" + json_placeorder_result["json_file_name_without_suffix"] + "_operate_history" + ".json"
    #
    with open(filename, 'w') as file_obj:
        json.dump(dict_operate_history, file_obj)
    #
    ###############################
    time.sleep(10)
    #
    #
    OcoManagement.getNowAllOcoList()
    result_orderListId = OcoManagement.getNowOcoListBySymbol("BTCUPUSDT")
    print(result_orderListId)
    OcoManagement.deleteOcoOderListBySymbolAndOrderListId("BTCUPUSDT", str(result_orderListId))
    #
    #

    #
    #

    #
    #


