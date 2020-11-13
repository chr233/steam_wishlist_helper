# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-11-07 21:12:39
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-13 15:32:20
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
    price_higher = 0
    price_lower = 0
    discount_higher = 0
    discount_lower = 0

    def __init__(self, setting: dict) -> None:
        '''
        初始化

        参数:
            setting: get_cfg()得到的配置字典
        '''
        def disable(x):
            return True
        price_set = setting.get('price_set', -1)
        price_noset = setting.get('price_noset', -1)
        price_free = setting.get('price_free', -1)
        price_higher = setting.get('price_higher', -1)
        price_lower = setting.get('price_lower', -1)

        discount_higher = setting.get('discount_higher', -1)
        discount_lower = setting.get('discount_lower', -1)
        discount_not_lowest = setting.get('discount_not_lowest', -1)
        discount_is_lowest = setting.get('discount_is_lowest', -1)
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

        if price_set or price_set == -1:
            self.__p_set = disable
        if price_noset or price_noset == -1:
            self.__p_noset = disable
        if price_free or price_free == -1:
            self.__p_free = disable
        if price_higher == -1:
            self.__p_higher = disable
        else:
            self.price_higher = price_higher
        if price_lower == -1:
            self.__p_lower = disable
        else:
            self.price_lower = price_lower

        if discount_higher == -1:
            self.__d_higher = disable
        else:
            self.discount_higher = discount_higher
        if discount_lower == -1:
            self.__d_lower = disable
        else:
            self.discount_lower = discount_lower
        if discount_not_lowest or discount_not_lowest == -1:
            self.__d_is_lowest = disable
        if discount_is_lowest or discount_is_lowest == -1:
            self.__d_not_lowest = disable
        if discount_almost_lowest or discount_is_lowest == -1:
            self.__d_almost_lowest = disable

    def filter(self, d: dict) -> bool:
        return self.__p_noset(d)

    def __p_set(self, d: dict) -> bool:
        '''
        过滤掉 有价格 的游戏
        '''
        free = d.get('free', False)

        if free:
            return True
        else:
            price = d.get('price', {})
            p_now = price.get('current', -1)
            return p_now == -1

    def __p_noset(self, d: dict) -> bool:
        '''
        过滤掉 没有价格 的游戏
        '''
        free = d.get('free', False)
        if free:
            return True
        else:
            price = d.get('price', {})
            p_now = price.get('current', -1)
            return p_now != -1

    def __p_free(self, d: dict) -> bool:
        '''
        过滤掉 免费 的游戏
        '''
        free = d.get('free', False)
        return free

    def __p_higher(self, d: dict) -> bool:
        '''
        过滤掉当前价格 低于 设定值的游戏
        '''
        free = d.get('free', False)
        if free:
            return True
        else:
            price = d.get('price', {})
            p_now = price.get('current', -1)
            if p_now == -1:
                return True
            else:
                return p_now >= self.price_higher

    def __p_lower(self, d: dict) -> bool:
        '''
        过滤掉当前价格 高于 设定值的游戏
        '''
        free = d.get('free', False)
        if free:
            return True
        else:
            price = d.get('price', {})
            p_now = price.get('current', -1)
            if p_now == -1:
                return True
            else:
                return p_now <= self.price_lower

    def __d_higher(self, d: dict) -> bool:
        '''
        过滤掉当前折扣 低于 设定值 的游戏
        '''
        free = d.get('free', False)
        if free:
            return True
        else:
            price = d.get('price', {})
            p_now = price.get('current', -1)
            if p_now == -1:
                return True
            else:
                return p_now >= self.discount_higher

    def __d_lower(self, d: dict) -> bool:
        '''
        过滤掉当前折扣 高于 设定值 的游戏
        '''
        free = d.get('free', False)
        if free:
            return True
        else:
            price = d.get('price', {})
            p_now = price.get('current', -1)
            if p_now == -1:
                return True
            else:
                return p_now <= self.discount_lower

    def __d_not_lowest(self, d: dict) -> bool:
        '''
        过滤掉 未达到 史低和近史低的游戏
        '''
        free = d.get('free', False)
        if free:
            return True
        else:
            price = d.get('price', {})
            is_lowest = price.get('is_lowest', 0)
            return is_lowest != 0

    def __d_is_lowest(self, d: dict) -> bool:
        '''
        过滤掉 达到 史低的游戏
        '''
        free = d.get('free', False)
        if free:
            return True
        else:
            price = d.get('price', {})
            is_lowest = price.get('is_lowest', 0)
            return is_lowest == 1

    def __d_almost_lowest(self, d: dict) -> bool:
        '''
        过滤掉 达到 近史低的游戏
        '''
        free = d.get('free', False)
        if free:
            return True
        else:
            price = d.get('price', {})
            is_lowest = price.get('is_lowest', 0)
            return is_lowest == -1
