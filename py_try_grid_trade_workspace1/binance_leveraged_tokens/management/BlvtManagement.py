from collections import OrderedDict

from mytool.MyUrlTool import RequestMethod
from client.MyClient import MyClient


class BlvtManagement:
    @staticmethod
    def getBlvtTokenInfoBySymbol(mySymbol):
        # myurl= 'https://api.binance.com/api/v3/ticker/price'
        # myurl = 'https://api.binance.com/sapi/v1/blvt/tokenInfo'
        myurl = 'https://api.binance.com'
        # myurl_resc_module = 'https://api.binance.com/sapi/v1/blvt/tokenInfo'
        myurl_resc_module = '/sapi/v1/blvt/tokenInfo'

        #dict_myparam = {'tokenName': 'BTCDOWN'}
        dict_myparam = {'tokenName': mySymbol}

        myheaders = {}
        #################################################
        myclient1 = MyClient()

        response = None
        try:
            response = myclient1.myrequest(RequestMethod.GET.value, headers=myheaders, url=myurl + myurl_resc_module,
                                           dict_myparam=dict_myparam, needSign=True)
        except Exception as e:
            print(f"error: request to {myurl + myurl_resc_module}, details:{e}")

        #
        if response is not None and response.status_code == 200:
            result_content = response.json()
            #
            print(response)
            print(result_content)
            #
            data = OrderedDict(result_content[0])
            first_ele = list(data.items())[1]
            # long_time = result_content['serverTime']
            print(first_ele)
            return result_content
        else:
            # do nothing
            print(response)
            return None