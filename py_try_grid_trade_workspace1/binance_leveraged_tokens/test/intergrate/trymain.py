import time

from myoco.management.OcoManagement import OcoManagement
from normalcheck.main import print_hi

if __name__ == '__main__':
    print_hi('PyCharm')

    dict_myparam = {'symbol': 'BTCUPUSDT', "side": "SELL",
                    "quantity": "0.31000000",
                    "price": "72", "stopPrice": "38", "stopLimitPrice": "39",
                    "stopLimitTimeInForce": "GTC"}
    OcoManagement.placeAnOcoOder(dict_myparam)
    #
    #
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


