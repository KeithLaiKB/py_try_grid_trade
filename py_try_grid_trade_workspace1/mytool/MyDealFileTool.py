import os
import pickle
import shutil


class MyDealFileTool:
    @staticmethod
    def getRootPath(str_projectName):
        project_path = os.path.abspath(os.path.dirname(__file__))
        print(project_path)
        #
        root_path = project_path[:project_path.find("{}\\".format(str_projectName)) + len("{}\\".format(str_projectName))]
        # root_path = '/home/pi/MyWorkspace/pycharm/py_play_workspace1/py_try_grid_trade/py_try_grid_trade_workspace1/'
        print('this project name：{}\r\nthis project root path：{}'.format(str_projectName, root_path))
        return root_path

    @staticmethod
    def mymkdir(path):
        # 去除首尾空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            print("create folder successfully: %s " % path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print
            path + ' 目录已存在'
            print("dir has already existed, create folder unsuccessfully: %s " % path)
            return False



    @staticmethod
    def myReadFile(path):
        data = ''
        with open(path, "r") as f:
            for line in f:
                data = data + line
            f.close()
        return data

    @staticmethod
    def myWriteFile(path, str):
        data = ''
        with open(path, "w") as f:
            f.write(str)
        return data

    @staticmethod
    def myCopyFile(srcfile, dstfile):
        #fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        #if not os.path.exists(fpath):
            #os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件