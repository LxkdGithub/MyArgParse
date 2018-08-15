#!/usr/bin/env python
# coding: utf-8


import argparse
import string
import threading
import zipfile
import os

#读取参数
parser = argparse.ArgumentParser(description='Here is the help!')
parser.add_argument('-i','--input',required=True, type=argparse.FileType('r'),dest='input_file', help='the zip-file you \'d like to explore')
parser.add_argument('-o','--output',type=argparse.FileType('w'),dest='output_file')
parser.add_argument('-l', '--length', type=int, choices=range(10))
parser.add_argument('-m', '--max_length', type=int, choices=range(10))

args = parser.parse_args()

# print('exists: ',os.path.exists(args.input_file.name))
# exit(0)


def check_file():
    global args
    if args.input_file:
        zipfile_name = args.input_file.name

        # 判断文件是否合法
        if os.path.exists(zipfile_name) and zipfile_name[-4:] == '.zip':
            try:
                zFile = zipfile.ZipFile(zipfile_name)
                return zFile
            except:
                exit(0)
        else:
            print('please input the correct filename of type zip')
            print(parser.format_usage())
            exit(0)
    else:
        print(parser.format_help())


#默认最大为10位
max_length = 10
if args.length:
    max_length = args.length
    length_exist = True
else:
    length_exist = False
    if args.max_length:
        max_length = args.max_length


length = 1   #默认从length = 1开始
print(max_length, length)
#提供爆破基
keys = string.ascii_uppercase+string.ascii_lowercase+string.digits+string.punctuation


def explore(zFile, passwd):
    print(passwd)
    try:
        print('begin..')
        zFile.extractall(pwd=passwd)
        print('[*] Found password %s' % passwd)
        return True
    except:
        return False


def loop_for(base_str, zFile):
    global length
    global max_length

    for i in keys:
        password = (base_str + i)
        print('password',password)
        if length_exist:
            print(length)
            if length == max_length:
                if explore(zFile, bytes(password,encoding='utf-8')):    #可用多线程
                    return True

            else:
                length += 1
                loop_for(password, zFile)

        else:
            print('no here')
            if explore(zFile, password):
                return True
            if length < max_length:
                length += 1
                loop_for(password, zFile)

    length -= 1
    return False


def main(zFile):

    # if length == 1:
    #     for i in keys:
    #         if explore(zFile, i):
    #             return True
    # else:
    loop_for('', zFile)


# if __name__ == "__main__":
#
zFile = check_file()
# zFile.extractall(pwd=b'12345')
# print(zFile.namelist())
main(zFile)








