# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-11-07 21:12:39
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-13 00:00:28
# @Description  : 过滤器模块【TODO】
'''


def game_filter(wishdict: dict, setting: dict) -> dict:
    '''
    根据配置过滤愿望单列表

    参数:
        wishdict: 愿望单字典
        setting: 过滤器配置节
    返回:
        dict: 过滤后的愿望单字典
    '''


class Filter(object):
    '''
    过滤器类
    '''

    def __init__(self, setting: dict) -> None:
        '''
        初始化

        参数:
            setting: get_cfg()得到的配置字典
        '''
        def disable(x):
            return True

        price_noset = setting.get('price_noset', -1)
        price_free = setting.get('price_free', -1)
        price_higher = setting.get('price_higher', -1)
        price_lower = setting.get('price_lower', -1)

        discount_higher = setting.get('discount_higher', -1)
        discount_lower = setting.get('discount_lower', -1)
        discount_reach_lowest = setting.get('discount_reach_lowest', -1)
        discount_almost_lowest = setting.get('discount_almost_lowest', -1)

        review_score_higher = setting.get('review_score_higher', -1)
        review_score_lower = setting.get('review_score_lower', -1)
        review_percent_higher = setting.get('review_percent_higher', -1)
        review_percent_lower = setting.get('review_percent_lower', -1)
        review_count_higher = setting.get('review_count_higher', -1)
        review_count_lower = setting.get('review_count_lower', -1)

        platform_windows = setting.get('platform_windows', -1)
        platform_mac = setting.get('platform_mac', -1)
        platform_linux = setting.get('platform_linux', -1)

        tags_include = setting.get('tags_include', -1)
        tags_exclude = setting.get('tags_exclude', -1)

        if price_noset == -1:
            self.__p_noset = disable
        else:
            self.price_noset = price_noset

    def filter(self, d: dict) -> bool:
        return self.__p_noset(d)

    def __p_noset(self, d: dict) -> bool:
        '''
        true:过滤掉 有价格 的游戏
        false:过滤掉 没有价格 的游戏
        '''
        price = d.get('price', {})
        p_now = price.get('current', -1)
        if self.price_noset:
            return p_now == -1
        else:
            return p_now != -1
