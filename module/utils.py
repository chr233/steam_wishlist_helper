# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-11-07 18:16:37
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-15 02:34:13
# @Description  : 一些公共函数
'''

from os import path, makedirs, getcwd

from .static import OP_PATH, ALMOST_LOWEST


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
        elif ((current - lowest) / origin <= ALMOST_LOWEST): # 近史低
            return -1
    return 0


def is_lowest_str(r: int) -> int:
    '''
    检查价格是否为史低

    参数:
        origin: 无折扣原价
        current: 现价
        lowest: 史低价
    返回:
        str: 史低/近史低/空文本
    '''
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


def dint(value: all, default: int = -1) -> int:
    '''
    带默认值的int()

    参数:
        value: 待转换值
        default: 默认值
    返回:
        int
    '''
    try:
        r = int(value)
    except (ValueError, TypeError):
        r = default
    return r


def fbool(value: all) -> bool:
    '''
    根据value,返回True,False或者-1

    参数:
        value: 待转换值
    返回:
        int
    '''
    value = dint(value, value)

    if value <= -1:
        return -1
    else:
        return bool(value)


def fint(value: all, max_: int = 0) -> int:
    '''
    根据value,返回大于0的整数,或者-1

    参数:
        value: 待转换值
        max_: 默认值
    返回:
        int
    '''
    value = dint(value, -1)

    if max_ > 0 and 0 <= value <= max_:
        return value
    elif max_ == 0 and 0 <= value:
        return value
    else:
        return -1


def flist(value: all) -> int:
    '''
    根据value,返回字符串列表

    参数:
        value: 待转换值
    返回:
        int
    '''
    value = dint(value, value)

    if value != -1:
        if isinstance(value, list):
            value = [str(x) for x in value]
        else:
            value = [str(value)]
    return value
