import json
import logging
import time



from binance_leveraged_tokens.management import BlvtManagement
from myoco.management.OcoManagement import OcoManagement
from mystradegy import MyStradegy1
from normalcheck.main import print_hi





if __name__ == '__main__':
    print_hi('PyCharm')
    logging.basicConfig(level=logging.INFO)

    mycoin_token                    = 'XRPUP'
    mycoin_symbol                   = 'XRPUPUSDT'
    mycoin_quantity                 = '1135.20'
    # 因为每个币的 小数不一样,
    # 如果后面运算以后 小数超过币安的设定, 会出现 Precision is over the maximum defined for this asset
    mycoin_precision                = 3

    initial_expected_profit_rate    = 0.03     # 相较于当前的myprice的 比例
    initial_expected_loss_rate      = 0.013     # 相较于当前的myprice的 比例
    after_expected_profit_rate      = 0.03     # 相较于当前的myprice的 比例
    after_expected_loss_rate        = 0.013     # 相较于当前的myprice的 比例
    #
    step_update_interval            = 0.01   # myprice=now_price 后进行 更新的幅度
    #
    gap_stoplimit_stoplimiprice     = 0.002   # myprice=now_price 后进行 更新的幅度
    #
    #my_midPrice                     = 0.08809
    my_midPrice                     = 4.680

    #
    #
    MyStradegy1.useStradegy1(mycoin_token, mycoin_symbol, mycoin_quantity, mycoin_precision,
                     initial_expected_profit_rate, initial_expected_loss_rate,
                     after_expected_profit_rate, after_expected_loss_rate,
                     step_update_interval, gap_stoplimit_stoplimiprice,
                     my_midPrice)

    #
    #

    #
    #


