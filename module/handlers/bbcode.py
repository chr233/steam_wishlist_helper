# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-07-06 18:22:37
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-08 12:52:30
# @Description  : 输出BBCode格式的文件
'''

from ..log import get_logger
from ..utils import is_lowest_str, get_output_path

logger = get_logger('BBCode')


def handler(wishdict: dict, symbol: str):
    '''
    这个函数将会被crawer调用

    参数:
        wishdict: 愿望单字典
    '''
    data = formater(wishdict, symbol)
    p = get_output_path('swh-bbcode.txt')
    with open(p, 'w+', encoding='utf-8') as f:
        f.write(data)
    logger.info(f'写入文件到 {p}')


def formater(wishdict: dict, symbol: str) -> str:
    '''
    这个函数用于从愿望单字典中提取数据

    参数:
        wishdict: 愿望单字典
    返回:
        str: 生成的结果
    '''
    result = []
    if wishdict:
        result.append(f'[table][tr][td]预览图[/td][td]游戏名称[/td][td]卡牌[/td]'
                      f'[td]现价({symbol})[/td][td]原价({symbol})[/td]'
                      f'[td]折扣[/td][td]史低({symbol})[/td][td]史低[/td][td]评测[/td][/tr]')
        for appid, detail in wishdict.items():
            link = f'https://store.steampowered.com/app/{appid}'
            name = detail.get('name', '')
            pic = detail.get('picture', '#')
            has_card = '有' if detail.get('has_card', False) else '无'
            if 'price_current' in detail:
                p_now = detail.get('price_current')
                p_old = detail.get('price_origion')
                p_cut = detail.get('price_cut')
                p_low = detail.get('price_lowest')
                shidi = is_lowest_str(p_old, p_now, p_low, p_cut)
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
            r_total = detail['review_total']
            # r_percent = detail['review_percent']
            review = f'{r_result} ({r_total})'
            # review = f'{r_result} {r_percent}%好评/({r_total})'

            result.append((f'[tr][td][url={link}][img]{pic}[/img][/url][/td]'
                           f'[td][url={link}]{name}[/url][/td]'
                           f'[td]{has_card}[/td]'
                           f'[td]{p_now}[/td]'
                           f'[td]{p_old}[/td]'
                           f'[td]{discount}[/td]'
                           f'[td]{p_low}[/td]'
                           f'[td]{shidi}[/td]'
                           f'[td]{review}[/td][/tr]'))
        result.append('[/table]')
    else:
        result.append('游戏列表空,请检查过滤器设置以及是否将愿望单公开')
    return ('\n'.join(result))
