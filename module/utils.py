# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-11-07 18:16:37
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-10 12:12:29
# @Description  : 一些公共函数
'''

from os import path, makedirs, getcwd
from math import ceil

from .static import OP_PATH


def is_lowest(origin: int, current: int, lowest: int, cut: int) -> int:
    '''
    检查价格是否为史低

    参数:
        origin: 无折扣原价
        current: 现价
        lowest: 史低价
    返回:
        int: 1-史低,0-未达史低也不是近史低,-1-近史低
    '''

    if (cut > 0):
        if (current <= lowest):  # 史低
            return 1
        elif ((current - lowest) < ceil(origin / 100)):  # 近史低

            return -1
    return 0


def is_lowest_str(origin: int, current: int, lowest: int, cut: int) -> int:
    '''
    检查价格是否为史低

    参数:
        origin: 无折扣原价
        current: 现价
        lowest: 史低价
    返回:
        str: 史低/近史低/空文本
    '''

    r = is_lowest(origin, current, lowest, cut)
    if (r > 0):
        return "史低"
    elif (r < 0):
        return "近史低"
    return "-"


def get_output_path(name: str) -> str:
    '''
    获取输出文件路径

    参数:
        name: 文件名
    返回:
        str: 文件路径
    '''
    if not path.exists(OP_PATH):
        makedirs(OP_PATH)
    p = path.join(getcwd(), OP_PATH, name)
    return str(p)

def aint(value:all,default:int=-1)->int:
    '''
    带默认值的int()

    参数:
        value: 待转换值
        default: 默认值
    返回:
        int
    '''
    try:    
        r=int(value)
    except ValueError:
        r=default
    return r

def fbool(value:all,default:int=-1)->int:
    '''
    带默认值的int()

    参数:
        value: 待转换值
        default: 默认值
    返回:
        int
    '''
    try:    
        r=int(value)
    except ValueError:
        r=default
    return r

def fint(value:all,default:int=-1)->int:
    '''
    带默认值的int()

    参数:
        value: 待转换值
        default: 默认值
    返回:
        int
    '''
    try:    
        r=int(value)
    except ValueError:
        r=default
    return r