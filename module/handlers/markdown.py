# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-07-06 18:22:37
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-14 14:41:53
# @Description  : 输出Markdown文件
'''

from ..log import get_logger
from ..utils import is_lowest_str, get_output_path

logger = get_logger('Markdown')


def handler(wishdict: dict, index: list, symbol: str):
    '''
    这个函数将会被crawer调用

    参数:
        wishdict: 愿望单字典
    '''
    data = formater(wishdict, index, symbol)
    p = get_output_path('swh-markdown.md')
    with open(p, 'w+', encoding='utf-8') as f:
        f.write(data)
    logger.info(f'写入文件到 {p}')


def formater(wishdict: dict, index: list, symbol: str) -> str:
    '''
    这个函数用于从愿望单字典中提取数据

    参数:
        wishdict: 愿望单字典
    返回:
        str: 生成的结果
    '''
    result = []
    result.append(
        f'|预览图|游戏名称|卡牌|现价({symbol})|原价({symbol})|折扣|史低({symbol})|史低|评测|')
    result.append('|-|-|-|-|-|-|-|-|-|')
    if wishdict:
        for appid, detail in wishdict.items():
            link = f'https://store.steampowered.com/app/{appid}'
            name = detail.get('name', '')
            pic = detail.get('picture', '#')
            has_card = '有' if detail.get('has_card', False) else '无'
            if 'price' in detail:
                price = detail['price']
                p_now = price.get('current')
                p_old = price.get('origion')
                p_cut = price.get('current_cut')
                p_low = price.get('lowest')
                shidi = is_lowest_str(price.get('is_lowest', 0))
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

            review = detail['review']
            r_result = review['result']
            r_total = review['total']
            # r_percent = review['percent']
            review_str = f'{r_result} ({r_total})'

            result.append((f'|[![]({pic})]({link})|[{name}]({link})|{has_card}|'
                           f'{p_now}|{p_old}|{discount}|{p_low}|{shidi}|{review_str}|'))
    else:
        result.append('游戏列表空,请检查过滤器设置以及是否将愿望单公开')
    return ('\n'.join(result))
