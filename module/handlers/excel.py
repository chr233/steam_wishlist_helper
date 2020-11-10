# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-07-06 18:22:37
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-08 14:32:58
# @Description  : 输出Xlsx文件
'''

from xlsxwriter import Workbook

from ..log import get_logger
from ..utils import is_lowest_str, get_output_path

logger = get_logger('Excel')


def handler(wishdict: dict, index: list, symbol: str):
    '''
    这个函数将会被crawer调用

    参数:
        wishdict: 愿望单字典
    '''
    p = get_output_path('swh-excel.xlsx')
    try:
        wb = Workbook(p)
        formater(wishdict, index, symbol, wb)
        wb.close()
    except Exception as e:
        logger.error(f'遇到意外错误 {e}')

    logger.info(f'写入文件到 {p}')


def formater(wishdict: dict, index: list, symbol: str, wb: Workbook):
    '''
    这个函数用于从愿望单字典中提取数据

    参数:
        wishdict: 愿望单字典
    '''

    fmt = wb.add_format({'font_name': '微软雅黑', 'align': 'center'})

    ws = wb.add_worksheet(name='Steam Wishlist Helper')
    ws.set_column('A:A', 10, fmt)
    ws.set_column('B:B', 60, fmt)
    ws.set_column('C:C', 7, fmt)
    ws.set_column('D:D', 8, fmt)
    ws.set_column('E:E', 8, fmt)
    ws.set_column('F:F', 7, fmt)
    ws.set_column('G:G', 8, fmt)
    ws.set_column('H:H', 8, fmt)
    ws.set_column('I:I', 12, fmt)
    ws.set_column('J:J', 7, fmt)
    ws.set_column('K:K', 9, fmt)
    ws.write(0, 0, '商店链接')
    ws.write(0, 1, '游戏名')
    ws.write(0, 2, '卡牌')
    ws.write(0, 3, f'现价({symbol})')
    ws.write(0, 4, f'原价({symbol})')
    ws.write(0, 5, '折扣')
    ws.write(0, 6, f'史低({symbol})')
    ws.write(0, 7, '史低')
    ws.write(0, 8, '评测结果')
    ws.write(0, 9, '好评率')
    ws.write(0, 10, '评测总数')
    if wishdict:
        for col, (appid, detail) in enumerate(wishdict.items(), 1):
            link = f'https://store.steampowered.com/app/{appid}'
            name = detail.get('name', '')
            has_card = '有' if detail.get('has_card', False) else '无'
            # pic = detail.get('picture', '#')
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
                p_old = '-'
                p_low = '-'

            r_result = detail['review_result']
            r_total = detail['review_total']
            r_percent = detail['review_percent']

            ws.write(col, 0, link)
            ws.write(col, 1, name)
            ws.write(col, 2, has_card)
            ws.write(col, 3, p_now)
            ws.write(col, 4, p_old)
            ws.write(col, 5, discount)
            ws.write(col, 6, p_low)
            ws.write(col, 7, shidi)
            ws.write(col, 8, r_result)
            ws.write(col, 9, f'{r_percent}%')
            ws.write(col, 10, r_total)
    else:
        ws.write(1, 1, '游戏列表空,请检查过滤器设置以及是否将愿望单公开')
