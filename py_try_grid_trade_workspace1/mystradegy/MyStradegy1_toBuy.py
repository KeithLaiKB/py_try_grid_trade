import json
import logging
import math
import time

from binance_leveraged_tokens.management import BlvtManagement
from myoco.management import OcoManagement


class MyStradegy1_toBuy:
    '''
    my_total_available 指的是 我可以用的金额
    然后根据 我可以用的钱来 计算coin_quantity

    '''
    @staticmethod
    def useStradegy1(coin_token, coin_symbol, quantity_precision, total_available, coin_precision,
                     init_expected_profit_rate, init_expected_loss_rate,
                     aft_expected_profit_rate, aft_expected_loss_rate,
                     stp_update_interval, gp_stoplimit_stoplimiprice,
                     mymidPrice):
        #logging.basicConfig(level=logging.INFO)
        logging.basicConfig(level=logging.DEBUG)

        '''
        mycoin_token = 'BTCDOWN'
        mycoin_symbol = 'BTCDOWNUSDT'
        mycoin_quantity = '1135.20'
        mycoin_precision = 5
        '''
        mycoin_token        = coin_token
        mycoin_symbol       = coin_symbol
        mycoin_quantity     = None
        mytotal_available   = total_available
        myquantity_precision= quantity_precision
        # 因为每个币的 小数不一样,
        # 如果后面运算以后 小数超过币安的设定, 会出现 Precision is over the maximum defined for this asset
        mycoin_precision    = coin_precision
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
        # 注意 这里和sell 不一样, sell 中 
        # my_price 是 你希望入的最低价
        #
        # stopLimitPrice
        # stopPrice 
        # 当前价格
        # midprice
        # price 
        #
        #
        # 如果当前价格 回升到我的stopPrice的时候 则会触发 我以一个stopLimitPrice(相对高的价格)去购买
        # 防止出现 币价 无法达到 price这个低价(相对低的价格), 从而买不到 的情况
        # 所以这里的my_midprice 是 1-0.05 而不是 像sell那样是 1 + 0.05
        #my_price            = my_midPrice * (1 - 0.05)
        #my_stopLimitPrice   = my_midPrice * (1 + 0.06)
        #my_stopPrice        = my_stopLimitPrice + 0.00005
        '''
        #
        my_price = my_midPrice * (1 - initial_expected_profit_rate)
        my_stopLimitPrice = my_midPrice * (1 + initial_expected_loss_rate)
        my_stopPrice = my_stopLimitPrice - gap_stoplimit_stoplimitprice

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
            mycoin_quantity = None
            #
            ############################ 获取 当前的价钱 ################################
            result_content = BlvtManagement.getBlvtTokenInfoBySymbol(mycoin_token)

            if result_content is not None:
                now_price = result_content[0]["nav"]
                now_price = float(now_price)
                print("price is", now_price)
            ###########################################################################
            # 如果是第一次运行, 先下一个卖OCO单
            if passFirstTime == False:
                # 因为我在用这个api的时候 我其实不会细算 我的 stoplimitprice是多少的, 因为我只设置了 rate
                # 防止 nowprice 此时 高于 my_midPrice,
                #                   并且接触到了 我的stopPrice, 然后又涨到我的 stoplimitprice是多少的  就买入了
                #                   从而导致 一挂单 就止损    买入了
                # 所以为了 保险起见, 我要求此时 now_price 一定要小于 my_midPrice, 才进行第一次挂单
                if now_price < my_midPrice:
                    ######################### 根据可用金额 计算要购买的数量 #########################
                    # 例如
                    # 我一共可用的金额是 12
                    # myquantity_precision 为2
                    #
                    # stopLimitPrice    51
                    # stopPrice         50
                    # 当前价格
                    # midprice
                    # price             45
                    #
                    # mycoin_quantity_tmp = 12/51 = 0.23529411764706.....
                    # 因为 myquantity_precision 为 2, 所以 mycoin_quantity_tmp 约等于0.24
                    # 然而 0.24 * 51 = 12.24 > 12
                    # 所以超出了 我的可用金额
                    # 所以我需要
                    # mycoin_quantity     = mycoin_quantity_tmp - 1/myquantity_precision
                    # mycoin_quantity     = 0.24                - 1/(10**myquantity_precision)
                    # mycoin_quantity     = 0.24                - 1/(10**2)
                    # mycoin_quantity     = 0.24                - 1/100
                    # mycoin_quantity     = 0.24                - 0.01
                    # mycoin_quantity     = 0.23
                    #
                    # 所以 0.23 * 51 = 11.73 < 12 不会超过 我的可用余额
                    #
                    mycoin_quantity_tmp = round(mytotal_available/my_stopLimitPrice, myquantity_precision)
                    mycoin_quantity     = mycoin_quantity_tmp - 1/(10**myquantity_precision)
                    #
                    ###########################################################################
                    #
                    dict_myparam = {'symbol': mycoin_symbol, "side": "BUY",
                                    "quantity": str(mycoin_quantity),
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
                # 如果当前价格 小于 我们的 之前的考量价
                #       则先 取消之前的订单, 再 重新下一个 新的OCO订单
                if now_price < my_midPrice:
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
                    # my_midPrice       = now_price - 0.001
                    my_midPrice         = now_price - step_update_interval

                    my_price            = my_midPrice * (1 - after_expected_profit_rate)
                    my_stopLimitPrice   = my_midPrice * (1 + after_expected_loss_rate)
                    # my_stopPrice      = my_stopLimitPrice -0.00005
                    my_stopPrice        = my_stopLimitPrice - gap_stoplimit_stoplimitprice

                    #######################Precision is over the maximum defined for this asset
                    my_midPrice = round(my_midPrice, mycoin_precision)

                    my_price = round(my_price, mycoin_precision)
                    my_stopLimitPrice = round(my_stopLimitPrice, mycoin_precision)
                    my_stopPrice = round(my_stopPrice, mycoin_precision)
                    ######################### 根据可用金额 计算要购买的数量 #########################
                    # 例如
                    # 我一共可用的金额是 12
                    # myquantity_precision 为2
                    #
                    # stopLimitPrice    51
                    # stopPrice         50
                    # 当前价格
                    # midprice
                    # price             45
                    #
                    # mycoin_quantity_tmp = 12/51 = 0.23529411764706.....
                    # 因为 myquantity_precision 为 2, 所以 mycoin_quantity_tmp 约等于0.24
                    # 然而 0.24 * 51 = 12.24 > 12
                    # 所以超出了 我的可用金额
                    # 所以我需要
                    # mycoin_quantity     = mycoin_quantity_tmp - 1/myquantity_precision
                    # mycoin_quantity     = 0.24                - 1/(10**myquantity_precision)
                    # mycoin_quantity     = 0.24                - 1/(10**2)
                    # mycoin_quantity     = 0.24                - 1/100
                    # mycoin_quantity     = 0.24                - 0.01
                    # mycoin_quantity     = 0.23
                    #
                    # 所以 0.23 * 51 = 11.73 < 12 不会超过 我的可用余额
                    #
                    mycoin_quantity_tmp = round(mytotal_available / my_stopLimitPrice, myquantity_precision)
                    mycoin_quantity = mycoin_quantity_tmp - 1 / (10 ** myquantity_precision)
                    ###########################################################################
                    ############## 获取这个币 已经下的订单(这个策略中 针对这个币 只做一个订单) #######################
                    OcoManagement.getNowAllOcoList()
                    result_orderListId = OcoManagement.getNowOcoListBySymbol(mycoin_symbol)
                    # 如果 订单    不存在, 就不做后续的操作了, 暂时来说不是什么大问题, 所以用 logging.DEBUG
                    if result_orderListId is None:
                        logging.log(logging.DEBUG, "could not find oco order lists with symbol({0})".format(mycoin_symbol))
                    # 如果 这个订单 存在
                    elif result_orderListId is not None:
                        ################# 先取消订单 ####################
                        print(result_orderListId)
                        delete_result_tmp = OcoManagement.deleteOcoOderListBySymbolAndOrderListId(mycoin_symbol,
                                                                                              str(result_orderListId))
                        logging.log(logging.INFO, "deleted result:{0}".format(delete_result_tmp))
                        ############ 按照新的设定 重新下单 ################
                        # 如果取消订单成功了, 才重新下单
                        if delete_result_tmp == 1:
                            dict_myparam = {'symbol': mycoin_symbol, "side": "BUY",
                                            "quantity": str(mycoin_quantity),
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