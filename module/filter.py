# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-11-07 21:12:39
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-15 03:00:52
# @Description  : 过滤器模块【TODO】
'''

class Filter(object):
    '''
    过滤器类
    '''
    price_higher = 0
    price_lower = 0
    discount_higher = 0
    discount_lower = 0
    review_score_higher = 0
    review_score_lower = 0
    review_percent_higher = 0
    review_percent_lower = 0
    review_total_higher = 0
    review_total_lower = 0
    tags_include = []
    tags_exclude = []

    def __init__(self, setting: dict) -> None:
        '''
        初始化

        参数:
            setting: get_cfg()得到的配置字典
        '''
        def disable(x):
            return True

        has_card = setting.get('has_card', -1)

        price_set = setting.get('price_set', -1)
        price_noset = setting.get('price_noset', -1)
        price_free = setting.get('price_free', -1)
        price_higher = setting.get('price_higher', -1)
        price_lower = setting.get('price_lower', -1)

        discount_no = setting.get('discount_no', -1)
        discount_higher = setting.get('discount_higher', -1)
        discount_lower = setting.get('discount_lower', -1)
        discount_not_lowest = setting.get('discount_not_lowest', -1)
        discount_is_lowest = setting.get('discount_is_lowest', -1)
        discount_almost_lowest = setting.get('discount_almost_lowest', -1)

        review_score_higher = setting.get('review_score_higher', -1)
        review_score_lower = setting.get('review_score_lower', -1)
        review_no_score = setting.get('review_no_score', -1)
        review_percent_higher = setting.get('review_percent_higher', -1)
        review_percent_lower = setting.get('review_percent_lower', -1)
        review_total_higher = setting.get('review_total_higher', -1)
        review_total_lower = setting.get('review_total_lower', -1)

        platform_windows = setting.get('platform_windows', -1)
        platform_mac = setting.get('platform_mac', -1)
        platform_linux = setting.get('platform_linux', -1)

        tags_enpty = setting.get('tags_enpty', -1)
        tags_include = setting.get('tags_include', -1)
        tags_exclude = setting.get('tags_exclude', -1)

        if not has_card or has_card == -1:  # 果过滤没有卡牌
            self.__o_has_card = disable

        if price_set or price_set == -1:  # 过滤有价格
            self.__p_set = disable
        if price_noset or price_noset == -1:  # 过滤无价格
            self.__p_noset = disable
        if price_free or price_free == -1:  # 过滤免费
            self.__p_free = disable
        if price_higher == -1:  # 过滤价格低于
            self.__p_higher = disable
        else:
            self.price_higher = price_higher
        if price_lower == -1:  # 过滤价格高于
            self.__p_lower = disable
        else:
            self.price_lower = price_lower

        if discount_no or discount_no == -1:  # 过滤未打折
            self.__d_no = disable
        if discount_higher == -1:  # 过滤折扣低于
            self.__d_higher = disable
        else:
            self.discount_higher = discount_higher
        if discount_lower == -1:  # 过滤折扣高于
            self.__d_lower = disable
        else:
            self.discount_lower = discount_lower
        if discount_not_lowest or discount_not_lowest == -1:  # 过滤非史低和非近史低
            self.__d_not_lowest = disable
        if discount_is_lowest or discount_is_lowest == -1:  # 过滤史低
            self.__d_is_lowest = disable
        if discount_almost_lowest or discount_is_lowest == -1:  # 过滤近史低
            self.__d_almost_lowest = disable

        if review_no_score or review_no_score == -1:  # 过滤无评测结果
            self.__r_no_score = disable
        if review_score_higher <= 0:  # 过滤评测等级低于
            self.__r_score_higher = disable
        else:
            self.review_score_higher = review_score_higher
        if review_score_lower <= 0:  # 过滤评测等级高于
            self.__r_score_lower = disable
        else:
            self.review_score_lower = review_score_lower
        if review_percent_higher == -1:  # 过滤好评率低于
            self.__r_percent_higher = disable
        else:
            self.review_percent_higher = review_percent_higher
        if review_percent_lower == -1:  # 过滤好评率高于
            self.__r_percent_lower = disable
        else:
            self.review_percent_lower = review_percent_lower
        if review_total_higher == -1:  # 过滤评测总数低于
            self.__r_total_higher = disable
        else:
            self.review_total_higher = review_total_higher
        if review_total_lower == -1:  # 过滤评测总数高于
            self.__r_total_lower = disable
        else:
            self.review_total_lower = review_total_lower

        if not platform_windows or platform_windows == -1:  # 过滤不支持win
            self.__p_windows = disable
        if not platform_mac or platform_mac == -1:  # 过滤不支持mac
            self.__p_mac = disable
        if not platform_linux or platform_linux == -1:  # 过滤不支持linux
            self.__p_linux = disable

        if tags_enpty or tags_enpty == -1:  # 过滤空标签
            self.__t_empty = disable
        if not tags_include or tags_include == -1:  # 过滤不包含指定标签
            self.__t_include = disable
        else:
            self.tags_include = tags_include
        if not tags_exclude or tags_exclude == -1:  # 过滤包含指定标签
            self.__t_exclude = disable
        else:
            self.tags_exclude = tags_exclude

    def filter(self, d: dict) -> bool:
        '''
        根据配置过滤愿望单列表
        '''
        result = (self.__o_has_card(d) and
                  self.__p_set(d) and
                  self.__p_noset(d) and self.__p_free(d) and
                  self.__p_higher(d) and self.__p_lower(d) and
                  self.__d_no(d) and
                  self.__d_higher(d) and self.__d_lower(d) and
                  self.__d_not_lowest(d) and
                  self.__d_is_lowest(d) and self.__d_almost_lowest(d) and
                  self.__r_no_score(d) and
                  self.__r_score_higher(d) and self.__r_score_lower(d) and
                  self.__r_percent_higher(d) and self.__r_percent_lower(d) and
                  self.__r_total_higher(d) and self.__r_total_lower(d) and
                  self.__p_windows(d) and
                  self.__p_mac(d) and self.__p_linux(d) and
                  self.__t_empty(d) and
                  self.__t_include(d) and self.__t_exclude(d))
        return result

    def __o_has_card(self, d: dict) -> bool:
        '''
        过滤掉 没有 卡牌的游戏
        '''
        card = d.get('card', False)
        return card  # 有卡有效

    def __p_set(self, d: dict) -> bool:
        '''
        忽略免费游戏
        过滤掉 有价格 的游戏
        '''
        price = d.get('price', {})
        p_now = price.get('current', -1)
        return p_now <= 0  # 免费或者无价格有效

    def __p_noset(self, d: dict) -> bool:
        '''
        忽略免费游戏
        过滤掉 没有价格 的游戏
        '''
        price = d.get('price', {})
        p_now = price.get('current', -1)
        return p_now >= 0  # 免费或者有价格有效

    def __p_free(self, d: dict) -> bool:
        '''
        过滤掉 免费 的游戏
        '''
        free = d.get('free', False)
        return not free  # 非免费有效

    def __p_higher(self, d: dict) -> bool:
        '''
        忽略免费和无价格的游戏
        过滤掉当前价格 低于 设定值的游戏
        '''
        price = d.get('price', {})
        p_now = price.get('current', -1)
        if p_now <= -0:
            return True  # 忽略免费或无价格
        else:
            return p_now >= self.price_higher  # 价格高于设定有效

    def __p_lower(self, d: dict) -> bool:
        '''
        忽略免费和无价格的游戏
        过滤掉当前价格 高于 设定值的游戏
        '''
        price = d.get('price', {})
        p_now = price.get('current', -1)
        if p_now <= 0:
            return True  # 忽略免费或无价格
        else:
            return p_now <= self.price_lower  # 价格低于设定有效

    def __d_no(self, d: dict) -> bool:
        '''
        过滤掉 未打折 的游戏
        '''
        price = d.get('price', {})
        p_cut = price.get('current_cut', -1)
        return p_cut > 0  # 打折有效

    def __d_higher(self, d: dict) -> bool:
        '''
        忽略未打折游戏
        过滤掉当前折扣 低于 设定值 的游戏
        '''
        price = d.get('price', {})
        p_cut = price.get('current_cut', -1)
        if p_cut == 0:
            return True  # 忽略未打折
        else:
            return p_cut >= self.discount_higher  # 折扣高于设定有效

    def __d_lower(self, d: dict) -> bool:
        '''
        忽略未打折游戏
        过滤掉当前折扣 高于 设定值 的游戏
        '''
        price = d.get('price', {})
        p_cut = price.get('current_cut', -1)
        if p_cut == 0:
            return True  # 忽略未打折
        else:
            return p_cut <= self.discount_lower  # 折扣低于设定有效

    def __d_not_lowest(self, d: dict) -> bool:
        '''
        忽略未打折游戏
        过滤掉 未达到 史低和近史低的游戏
        '''
        price = d.get('price', {})
        p_cut = price.get('current_cut', -1)
        if p_cut == 0:
            return True  # 忽略未打折
        else:
            is_lowest = price.get('is_lowest', 0)
            return is_lowest != 0  # 史低或近史低有效

    def __d_is_lowest(self, d: dict) -> bool:
        '''
        忽略未打折游戏
        过滤掉 达到 史低的游戏
        '''
        price = d.get('price', {})
        p_cut = price.get('current_cut', -1)
        if p_cut == 0:
            return True  # 忽略未打折
        else:
            is_lowest = price.get('is_lowest', 0)
            return is_lowest != 1  # 非史低或近史低有效

    def __d_almost_lowest(self, d: dict) -> bool:
        '''
        忽略未打折游戏
        过滤掉 达到 近史低的游戏
        '''
        price = d.get('price', {})
        p_cut = price.get('current_cut', -1)
        if p_cut == 0:
            return True  # 忽略未打折
        else:
            is_lowest = price.get('is_lowest', 0)
            return is_lowest != -1  # 非史低或史低有效

    def __r_no_score(self, d: dict) -> bool:
        '''
        过滤掉 评价等级 = 0 的游戏
        '''
        review = d.get('review', {})
        score = review.get('score', -1)
        return score > 0  # 评分低于0有效

    def __r_score_higher(self, d: dict) -> bool:
        '''
        忽略评价等级 = 0 的游戏
        过滤掉评价等级 低于 设定值的游戏
        '''
        review = d.get('review', {})
        score = review.get('score', -1)

        if score <= 0:
            return True  # 忽略没评价或出错
        else:
            return score >= self.review_score_higher  # 评分高于设定有效

    def __r_score_lower(self, d: dict) -> bool:
        '''
        忽略评价等级 = 0 的游戏
        过滤掉评价等级 高于 设定值的游戏
        '''
        review = d.get('review', {})
        score = review.get('score', -1)

        if score <= 0:
            return True  # 忽略没评价或出错
        else:
            return score <= self.review_score_lower  # 评分低于设定有效

    def __r_percent_higher(self, d: dict) -> bool:
        '''
        过滤掉好评率 低于 设定值的游戏
        '''
        review = d.get('review', {})
        score = review.get('score', -1)

        if score <= 0:
            return True  # 忽略没评价或出错
        else:
            percent = review.get('percent', -1)
            return percent >= self.review_percent_higher  # 评分低于设定有效

    def __r_percent_lower(self, d: dict) -> bool:
        '''
        过滤掉好评率 低于 设定值的游戏
        '''
        review = d.get('review', {})
        score = review.get('score', -1)

        if score <= 0:
            return True  # 忽略没评价或出错
        else:
            percent = review.get('percent', -1)
            return percent <= self.review_percent_lower  # 评分低于设定有效

    def __r_total_higher(self, d: dict) -> bool:
        '''
        过滤掉评价总数 低于 设定值的游戏
        '''
        review = d.get('review', {})
        score = review.get('score', -1)

        if score <= 0:
            return True  # 忽略没评价或出错
        else:
            total = review.get('total', -1)
            return total >= self.review_total_higher  # 评价总数低于设定有效

    def __r_total_lower(self, d: dict) -> bool:
        '''
        过滤掉评价总数 低于 设定值的游戏
        '''
        review = d.get('review', {})
        score = review.get('score', -1)

        if score <= 0:
            return True  # 忽略没评价或出错
        else:
            total = review.get('total', -1)
            return total <= self.review_total_lower  # 评价总数低于设定有效

    def __p_windows(self, d: dict) -> bool:
        '''
        过滤掉 不支持 Windows的游戏
        '''
        windows, _, _ = d.get('platform', (False, False, False))
        return windows  # 支持win有效

    def __p_mac(self, d: dict) -> bool:
        '''
        过滤掉 不支持 Mac的游戏
        '''
        _, macos, _ = d.get('platform', (False, False, False))
        return macos  # 支持mac有效

    def __p_linux(self, d: dict) -> bool:
        '''
        过滤掉 不支持 Linux的游戏
        '''
        _, _, linux = d.get('platform', (False, False, False))
        return linux  # 支持linux有效

    def __t_empty(self, d: dict) -> bool:
        '''
        过滤掉 没有 标签的游戏
        '''
        tags = d.get('tags', [])
        return bool(tags)  # 含有标签有效

    def __t_include(self, d: dict) -> bool:
        '''
        忽略没有标签的游戏
        过滤掉标签 不匹配 规则的游戏
        '''
        itags = self.tags_include
        tags = d.get('tags', [])
        if not tags:
            return True  # 含有标签有效
        for it in itags:
            flag = False
            for t in tags:
                if it in t:
                    flag = True
                    break
            if not flag:
                return False
        return True  # 包含全部标签有效

    def __t_exclude(self, d: dict) -> bool:
        '''
        忽略没有标签的游戏
        过滤掉标签 匹配 规则的游戏
        '''
        itags = self.tags_include
        tags = d.get('tags', [])
        if not tags:
            return True  # 含有标签有效
        for it in itags:
            flag = False
            for t in tags:
                if it in t:
                    flag = True
                    break
            if flag:
                return False
        return True  # 不包含全部标签有效
