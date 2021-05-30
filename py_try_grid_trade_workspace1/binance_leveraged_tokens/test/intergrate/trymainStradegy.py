import time

from binance_leveraged_tokens.management import BlvtManagement
from myoco.management.OcoManagement import OcoManagement
from normalcheck.main import print_hi





if __name__ == '__main__':
    print_hi('PyCharm')

    #
    # 假设没挂单
    #
    # 当价格达到 0.09500时, 若到不了就不卖
    # 挂一个
    #
    # price                      0.10000
    # 此时价格                    0.09500
    # stop price                 0.09005
    # stop limit price           0.09000
    #
    # 如果
    # 此时价格              0.09500 == old_midPrice
    #
    # price                     0.10000        +0.00500     = 0.10500
    #
    # midPrice                  0.09500        +0.00500     = 0.10000
    #                       此时价格                            0.09500
    #
    # stop limit price          0.09000        +0.00200     = 0.09200
    # stop price(trigger)       0.09005        +0.00005     = 0.09205

    #
    # 也就是说
    # price                         和 midPrice                  相差0.05000
    # stop limit price_old          和 stop limit price_new      相差0.05000
    # stop price                    和 stop limit price_new      相差0.00005
    '''
    my_price            = 0.01

    my_midPrice         = 0.09500

    my_stopPrice        = 0.09005
    my_stopLimitPrice   = 0.09000
    '''
    #
    #my_midPrice         = 0.06700
    my_midPrice          = 0.06600

    my_price            = my_midPrice * (1 + 0.05)
    my_stopLimitPrice   = my_midPrice * (1 - 0.06)
    my_stopPrice        = my_stopLimitPrice + 0.00005

    #######################Precision is over the maximum defined for this asset
    my_midPrice = round(my_midPrice, 5)

    my_price = round(my_price, 5)
    my_stopLimitPrice = round(my_stopLimitPrice, 5)
    my_stopPrice = round(my_stopPrice, 5)
    print("kkkkkk", my_midPrice,my_price,my_stopLimitPrice,my_stopPrice)

    passFirstTime = False
    while True:
        result_content = BlvtManagement.getBlvtTokenInfoBySymbol("BTCDOWN")

        now_price = result_content[0]["nav"]
        now_price = float(now_price)
        print("price is", now_price)
        ###########################################################################
        if passFirstTime == False:
            if now_price > my_midPrice:
                dict_myparam = {'symbol': 'BTCDOWNUSDT', "side": "SELL",
                                "quantity": "1135.20",
                                "price": str(my_price), "stopPrice": str(my_stopPrice), "stopLimitPrice": str(my_stopLimitPrice),
                                "stopLimitTimeInForce": "GTC"}
                OcoManagement.placeAnOcoOder(dict_myparam)
                #
                passFirstTime = True
            #
        #
        elif passFirstTime == True:
            if now_price > my_midPrice:
                print("##########################################now{},old{}", now_price, my_midPrice)
                ##############设定新值#######################
                '''
                # 目标中间值 上升 0.005
                my_midPrice       = my_midPrice + 0.00500
                
                #
                # 其他以此为参考标准 进行调整
                my_price            = my_midPrice + 0.00500
                my_stopLimitPrice   = my_stopLimitPrice + 0.00200
                my_stopPrice        = my_stopLimitPrice + 0.00005
                '''
                #my_midPrice         = now_price   #调试用 因为这样的话 很快my_midPrice就会更新
                my_midPrice         = now_price + 0.002

                my_price            = my_midPrice * (1 + 0.05)
                my_stopLimitPrice   = my_midPrice * (1 - 0.06)
                my_stopPrice        = my_stopLimitPrice +0.00005

                #######################Precision is over the maximum defined for this asset
                my_midPrice         = round(my_midPrice,5)

                my_price            = round(my_price,5)
                my_stopLimitPrice   = round(my_stopLimitPrice,5)
                my_stopPrice        = round(my_stopPrice,5)

                ############先取消订单#################
                OcoManagement.getNowAllOcoList()
                result_orderListId = OcoManagement.getNowOcoListBySymbol("BTCDOWNUSDT")
                print(result_orderListId)
                delete_result_tmp = OcoManagement.deleteOcoOderListBySymbolAndOrderListId("BTCDOWNUSDT", str(result_orderListId))
                print("##########################################", delete_result_tmp)
                ############按照新的设定 重新下单#################
                if delete_result_tmp == 1:
                    dict_myparam = {'symbol': 'BTCDOWNUSDT', "side": "SELL",
                                    "quantity": "1135.20",
                                    "price": str(my_price), "stopPrice": str(my_stopPrice), "stopLimitPrice": str(my_stopLimitPrice),
                                    "stopLimitTimeInForce": "GTC"}
                    OcoManagement.placeAnOcoOder(dict_myparam)
        time.sleep(5)

    #
    #

    #
    #


