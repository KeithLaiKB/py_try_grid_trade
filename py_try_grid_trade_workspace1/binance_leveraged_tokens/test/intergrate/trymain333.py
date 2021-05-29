import time

from myoco.BlvtManagement import BlvtManagement
from normalcheck.main import print_hi





if __name__ == '__main__':
    print_hi('PyCharm')

    #
    #
    while True:
        result_content = BlvtManagement.getBlvtTokenInfoBySymbol("BTCDOWN")

        price = result_content[0]["nav"]
        print("price is", price)
        time.sleep(5)
    #
    #

    #
    #


