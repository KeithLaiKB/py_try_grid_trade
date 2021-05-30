import hashlib
import hmac
import json

from pip._vendor import requests

from mytool.MyDealFileTool import MyDealFileTool
from mytool.MyUrlTool import MyUrlTool, RequestMethod



class MyClient(object):  # 创建Circle类
    __myurl = None
    __myapi_resc_module = None

    __apiKey = None
    __sctKey = None

    __myheaders_apikey = None

    #
    def __init__(self, url=None, api_resc_module=None):
        #
        self.__myurl = url
        self.__myapi_resc_module = api_resc_module
        ############################ load binance key  #####################################################
        ############ get path of binance key json file ###############
        #
        #
        ###### method one ######
        #root_path = '/home/pi/MyWorkspace/pycharm/py_play_workspace1/py_try_grid_trade/py_try_grid_trade_workspace1'
        ###### method two ######
        '''
        my_project_name = 'py_try_grid_trade_workspace1'
        project_path = os.path.abspath(os.path.dirname(__file__))
        print(project_path)
        root_path = project_path[:project_path.find("{}\\".format(my_project_name)) + len("{}\\".format(my_project_name))]
        print('this project name：{}\r\nthis project root path：{}'.format(my_project_name, root_path))
        '''
        my_project_name = 'py_try_grid_trade_workspace1'
        root_path = MyDealFileTool.getRootPath(my_project_name)
        #
        #
        ############ get json content from json file ###############
        str_binance_key = MyDealFileTool.myReadFile(root_path + r"/personal/binance_key/mykey.json")
        json_binance_key = json.loads(str_binance_key)
        #
        self.__apiKey = json_binance_key["binance_api_key"]
        self.__sctKey = json_binance_key["binance_secret_key"]
        #
        self.__myheaders_apikey = {"X-MBX-APIKEY" : self.__apiKey}
        print(self.__myheaders_apikey)
        ###################################################################################################
        print("client initiated")


    def myrequest(self, reqMethod:RequestMethod, url, headers=None,  dict_myparam=None, needSign=False):
        if headers == None:
            headers = self.__myheaders_apikey
        elif headers != None:
            headers.update(self.__myheaders_apikey)
            print("hey my header is",headers)
        # 把一组参数字典{参数名1=参数值1, 参数名2=参数值2, 参数名3=参数值3}
        # 弄成字符串             &参数名1=参数值1 &参数名2=参数值2 &参数名3=参数值3  (正常来说 是没有空格的, 只是这里为了你看起来舒服而已)
        # 也就是说
        # 参数名1=参数值1&参数名2=参数值2&参数名3=参数值3
        str_urlParam = MyUrlTool.convertDictToUrlParameter(myparams=dict_myparam)
        #
        #
        # 然后用 secretkey 把 上面的请求字符串 进行加密
        # 弄成字符串 secretkey值  参数名1=参数值1 &参数名2=参数值2 &参数名3=参数值3 (正常来说 是没有空格的, 只是这里为了你看起来舒服而已)
        # 也就是说
        # 用 secretkey值 把 参数名1=参数值1&参数名2=参数值2&参数名3=参数值3 进行加密
        #
        # 然后进行整体加密，成为 签名值( secretkey值和 请求参数值 整体加密后的结果)
        # 用 secretkey值 把 参数名1=参数值1&参数名2=参数值2&参数名3=参数值3  ====整体加密后形成====>  签名值
        hexdigest = hmac.new(self.__sctKey.encode('utf8'), str_urlParam.encode("utf-8"), hashlib.sha256).hexdigest()
        #
        # 然后再和 前面的参数进行整体 的结合
        # 弄成字符串 &参数名1=参数值1 &参数名2=参数值2 &参数名3=参数值3 &signature=签名值(利用secretkey值 把 请求参数值 整体加密后的结果)  (正常来说 是没有空格的, 只是这里为了你看起来舒服而已)
        # 也就是说
        # 参数名1=参数值1&参数名2=参数值2&参数名3=参数值3&signature=签名值(secretkey值和 请求参数值 整体加密后的结果)
        str_urlParam_with_sig = str_urlParam + '&signature=' + str(hexdigest)
        #
        # 然后结合url
        # 得到
        # https://api.binance.com/sapi/v1/blvt/tokenInfo?参数名1=参数值1&参数名2=参数值2&参数名3=参数值3&signature=签名值(secretkey值和 请求参数值 整体加密后的结果)
        if dict_myparam == None or bool(dict_myparam)==False or needSign==False:
            req_url = url
        else:
            req_url = url + '?' + str_urlParam_with_sig
        #
        response = None
        try:
            print("sending request to", req_url)
            response = requests.request(reqMethod, headers=headers, url=req_url)
        except Exception as e:
            print(f"error: request to {req_url}, details:{e} in MyClient.myrequest")
        return response