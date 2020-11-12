# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-07-05 12:43:38
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-12 18:57:42
# @Description  : 在控制台输出
'''

from prettytable import PrettyTable

from ..log import get_logger
from ..utils import is_lowest_str

logger = get_logger('Console')


def handler(wishdict: dict, index: list, symbol: str) -> str:
    '''
    这个函数将会被crawer调用

    参数:
        wishdict: 愿望单字典
    '''
    logger.info('开始打印'.center(50, '='))
    data = formater(wishdict, index, symbol)
    print(data)
    logger.info('打印结束'.center(50, '='))


def formater(wishdict: dict, index: list, symbol: str) -> PrettyTable:
    '''
    这个函数用于从愿望单字典中提取数据

    参数:
        wishdict: 愿望单字典
    返回:
        str: 生成的结果
    '''
    table = PrettyTable(
        ['游戏名称', '卡牌', f'现价({symbol})', f'原价({symbol})', '折扣',  '史低', '评测结果'])
    if wishdict:
        for appid, detail in wishdict.items():
            # link = f'https://store.steampowered.com/app/{appid}'
            name = str(detail.get('name', ''))
            # pic = detail.get('picture', '#')
            has_card = '有' if detail.get('has_card', False) else '无'
            if 'price' in detail:
                price = detail['price']
                p_now = price.get('current')
                p_old = price.get('origion')
                p_cut = price.get('current_cut')
                p_low = price.get('lowest')
                shidi = is_lowest_str(price.get('is_lowest',0))
                discount = f'-{p_cut}%'
            else:
                shidi = '-'
                discount = '-'
                p_now = '-'
                p_low = '-'
                p_old = '-'
            if detail['free']:
                p_now = '免费'
                shidi = '免费'
                p_low = '免费'
                p_old = '免费'
            if p_now == -1:
                p_now = '-'
                p_low = '-'
                p_old = '-'

            r_result = detail['review_result']
            # r_total = detail['review_total']
            # r_percent = detail['review_percent']
            # review = f'{r_result} ({r_total})'
            # review = f'{r_result} {r_percent}%好评/({r_total})'
            if '史低' in shidi:
                table.add_row([name, has_card, p_now, p_old,
                               discount,  shidi, r_result])
    else:
        table.add_row(['游戏列表空,请检查过滤器设置以及是否将愿望单公开', '', '', ''])
    return (table)
