import json
import logging
import time

from binance_leveraged_tokens.management import BlvtManagement
from myoco.management import OcoManagement


class MyStradegy1:
    @staticmethod
    def useStradegy1(coin_token, coin_symbol, coin_quantity, coin_precision,
                     init_expected_profit_rate, init_expected_loss_rate,
                     aft_expected_profit_rate, aft_expected_loss_rate,
                     stp_update_interval, gp_stoplimit_stoplimiprice,
                     mymidPrice):
        logging.basicConfig(level=logging.INFO)
        '''
        mycoin_token = 'BTCDOWN'
        mycoin_symbol = 'BTCDOWNUSDT'
        mycoin_quantity = '1135.20'
        mycoin_precision = 5
        '''
        mycoin_token    = coin_token
        mycoin_symbol   = coin_symbol
        mycoin_quantity = coin_quantity
        # 因为每个币的 小数不一样,
        # 如果后面运算以后 小数超过币安的设定, 会出现 Precision is over the maximum defined for this asset
        mycoin_precision = coin_precision
        #
        #
        #
        '''
        initial_expected_profit_rate    = 0.018  # 相较于当前的myprice的 比例
        initial_expected_loss_rate      = 0.018  # 相较于当前的myprice的 比例
        after_expected_profit_rate      = 0.018  # 相较于当前的myprice的 比例
        after_expected_loss_rate        = 0.018  # 相较于当前的myprice的 比例
        #
        step_update_interval            = 0.00020  # myprice=now_price 后进行 更新的幅度
        #
        gap_stoplimit_stoplimitprice    = 0.00005  # myprice=now_price 后进行 更新的幅度
        #
        my_midPrice                     = 0.08809
        '''
        #
        initial_expected_profit_rate    = init_expected_profit_rate     # 相较于当前的myprice的 比例
        initial_expected_loss_rate      = init_expected_loss_rate       # 相较于当前的myprice的 比例
        after_expected_profit_rate      = aft_expected_profit_rate      # 相较于当前的myprice的 比例
        after_expected_loss_rate        = aft_expected_loss_rate        # 相较于当前的myprice的 比例
        #
        step_update_interval            = stp_update_interval           # myprice=now_price 后进行 更新的幅度
        #
        gap_stoplimit_stoplimitprice    = gp_stoplimit_stoplimiprice    # myprice=now_price 后进行 更新的幅度
        #
        my_midPrice                     = mymidPrice


        '''
        #my_price            = my_midPrice * (1 + 0.05)
        #my_stopLimitPrice   = my_midPrice * (1 - 0.06)
        #my_stopPrice        = my_stopLimitPrice + 0.00005
        '''
        #
        my_price = my_midPrice * (1 + initial_expected_profit_rate)
        my_stopLimitPrice = my_midPrice * (1 - initial_expected_loss_rate)
        my_stopPrice = my_stopLimitPrice + gap_stoplimit_stoplimitprice

        #######################Precision is over the maximum defined for this asset
        my_midPrice = round(my_midPrice, mycoin_precision)

        my_price = round(my_price, mycoin_precision)
        my_stopLimitPrice = round(my_stopLimitPrice, mycoin_precision)
        my_stopPrice = round(my_stopPrice, mycoin_precision)
        #
        logging.log(logging.INFO,
                    "mymidprice:{0},my_price:{1},my_stopLimitPrice:{2},my_stopPrice:{3}".format(my_midPrice, my_price,
                                                                                                my_stopLimitPrice,
                                                                                                my_stopPrice))
        #
        passFirstTime = False
        while True:
            json_result = None
            ############################ 获取 当前的价钱 ################################
            result_content = BlvtManagement.getBlvtTokenInfoBySymbol(mycoin_token)

            if result_content is not None:
                now_price = result_content[0]["nav"]
                now_price = float(now_price)
                print("price is", now_price)
            ###########################################################################
            # 如果是第一次运行, 先下一个卖OCO单
            if passFirstTime == False:
                if now_price > my_midPrice:
                    dict_myparam = {'symbol': mycoin_symbol, "side": "SELL",
                                    "quantity": mycoin_quantity,
                                    "price": str(my_price), "stopPrice": str(my_stopPrice),
                                    "stopLimitPrice": str(my_stopLimitPrice),
                                    "stopLimitTimeInForce": "GTC"}
                    #
                    json_placeorder_result = OcoManagement.placeAnOcoOder(dict_myparam)
                    ######### record operation history#############
                    print(json_placeorder_result["result"])
                    print(json_placeorder_result["json_file_path"])
                    print(json_placeorder_result["json_file_name_without_suffix"])
                    #
                    # if it places order successfully, then record it in a file
                    if json_placeorder_result["result"] == 1:
                        dict_operate_history = {'symbol': mycoin_symbol,
                                                "midprice": my_midPrice,
                                                "price": my_price,
                                                "stopPrice": my_stopPrice,
                                                "stopLimitPrice": my_stopLimitPrice
                                                }
                        filename = json_placeorder_result["json_file_path"] + "/" + json_placeorder_result[
                            "json_file_name_without_suffix"] + "_operate_history" + ".json"
                        #
                        with open(filename, 'w') as file_obj:
                            json.dump(dict_operate_history, file_obj)
                        #################################################
                        passFirstTime = True
                #
            #
            ###########################################################################
            # 如果不是第一次运行
            elif passFirstTime == True:
                # 如果当前价格 大于 我们的 之前的考量价
                #       则先 取消之前的订单, 再 重新下一个 新的OCO订单
                if now_price > my_midPrice:
                    logging.log(logging.INFO, "nowPrice_new:{0},my_midPrice_old:{1}".format(now_price, my_midPrice))

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
                    # my_midPrice       = now_price   #调试用 因为这样的话 很快my_midPrice就会更新
                    # my_midPrice       = now_price + 0.001
                    my_midPrice         = now_price + step_update_interval

                    my_price            = my_midPrice * (1 + after_expected_profit_rate)
                    my_stopLimitPrice   = my_midPrice * (1 - after_expected_loss_rate)
                    # my_stopPrice      = my_stopLimitPrice +0.00005
                    my_stopPrice        = my_stopLimitPrice + gap_stoplimit_stoplimitprice

                    #######################Precision is over the maximum defined for this asset
                    my_midPrice = round(my_midPrice, mycoin_precision)

                    my_price = round(my_price, mycoin_precision)
                    my_stopLimitPrice = round(my_stopLimitPrice, mycoin_precision)
                    my_stopPrice = round(my_stopPrice, mycoin_precision)

                    ############先取消订单#################
                    OcoManagement.getNowAllOcoList()
                    result_orderListId = OcoManagement.getNowOcoListBySymbol(mycoin_symbol)
                    print(result_orderListId)
                    delete_result_tmp = OcoManagement.deleteOcoOderListBySymbolAndOrderListId(mycoin_symbol,
                                                                                              str(result_orderListId))
                    logging.log(logging.INFO, "deleted result:{0}".format(delete_result_tmp))
                    ############按照新的设定 重新下单#################
                    if delete_result_tmp == 1:
                        dict_myparam = {'symbol': mycoin_symbol, "side": "SELL",
                                        "quantity": mycoin_quantity,
                                        "price": str(my_price), "stopPrice": str(my_stopPrice),
                                        "stopLimitPrice": str(my_stopLimitPrice),
                                        "stopLimitTimeInForce": "GTC"}
                        json_placeorder_result = OcoManagement.placeAnOcoOder(dict_myparam)
                        ######### record operation history#############
                        print(json_placeorder_result["result"])
                        print(json_placeorder_result["json_file_path"])
                        print(json_placeorder_result["json_file_name_without_suffix"])
                        #
                        # if it places order successfully, then record it in a file
                        if json_placeorder_result["result"] == 1:
                            dict_operate_history = {'symbol': mycoin_symbol,
                                                    "midprice": my_midPrice,
                                                    "price": my_price,
                                                    "stopPrice": my_stopPrice,
                                                    "stopLimitPrice": my_stopLimitPrice
                                                    }
                            filename = json_placeorder_result["json_file_path"] + "/" + json_placeorder_result[
                                "json_file_name_without_suffix"] + "_operate_history" + ".json"
                            #
                            with open(filename, 'w') as file_obj:
                                json.dump(dict_operate_history, file_obj)
                        #################################################
            #
            time.sleep(3)