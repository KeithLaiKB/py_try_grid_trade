# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from collections import OrderedDict

########################################################
from mytool.MyClient import MyClient
from MyUrlTool import RequestMethod

#myheaders = {"a": 'b'}
myheaders = {}

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.








if __name__ == '__main__':
    print_hi('PyCharm')
    #myurl= 'https://api.binance.com/api/v3/ticker/price'
    #myurl = 'https://api.binance.com/sapi/v1/blvt/tokenInfo'
    myurl = 'https://api.binance.com'
    #myurl_resc_module = 'https://api.binance.com/sapi/v1/blvt/tokenInfo'
    myurl_resc_module = '/sapi/v1/blvt/tokenInfo'

    dict_myparam = {'tokenName' : '1INCHUP'}
    myclient1=MyClient()

    response = None
    try:
        response = myclient1.myrequest(RequestMethod.GET.value,headers=myheaders, url=myurl+myurl_resc_module, dict_myparam=dict_myparam)
    except Exception as e:
        print(f"error: request to {myurl+myurl_resc_module}, details:{e}")

    #
    if response.status_code == 200:
        result_content = response.json()
        #
        print(response)
        print(result_content)
        #
        data = OrderedDict(result_content[0])
        first_ele = list(data.items())[1]
        #long_time = result_content['serverTime']
        print(first_ele)
    else:
        # do nothing
        print(response)
