# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-11-02 20:56:28
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-15 03:08:44
# @Description  : 抓取模块
'''
from asyncio import Semaphore

from .log import get_logger
from .aiosteam import get_wishlish
from .aioitad import get_plains, get_lowest_price, get_current_price, get_base_info
from .aiokeylol import get_games_tags
from .handlers import bbcode, markdown, excel, json  # , console
from .sort import get_index
from .filter import Filter
from .utils import is_lowest


class Crawer(object):

    wishdict = {}  # {appid: {游戏详情}}
    steamids = {}  # steam账号列表
    setting = {}   # 配置
    index = []     # 索引

    def __init__(self, setting: dict, steamids: list, tag: str = None) -> None:
        '''
        初始化抓取器

        参数:
            config: 调用module.config.get_config()获取
            steamids: steamid列表
        '''
        try:
            steamids = set(steamids)
        except TypeError:
            raise ValueError('steam ID必须为非空列表')

        if steamids:
            self.steamids = steamids
            self.setting = setting

            self.logger = get_logger(f'Crawer *{len(steamids)}')
            self.logger.debug(f'共有{len(steamids)}个账号')
        else:
            raise ValueError('steam ID必须为非空列表')

    async def start(self):
        async with Semaphore(3):  # 最大并发数
            await self.get_wishlist()
            await self.add_price()
            await self.add_addition()
            self.filter()
            # self.sort()
            self.output()

    async def get_wishlist(self):
        '''
        从steam读取愿望单
        '''
        wishdict = self.wishdict
        setting = self.setting
        steamids = self.steamids

        net = setting.get('net', {})
        proxy = net.get('proxy', None)

        self.logger.info('开始读取愿望单,如果一直报错请配置proxy')
        for i, sid in enumerate(steamids, 1):
            self.logger.info(f'开始读取 {steamids} 的愿望单 {i}')
            dic = await get_wishlish(sid, setting, proxy)
            self.logger.info(f'读取完毕,愿望单中共有{len(dic)}个游戏')
            wishdict.update(dic)
        self.logger.info(f'愿望单读取完毕,合并后共有{len(wishdict)}个游戏')

    async def add_price(self):
        '''
        获取游戏价格信息
        '''
        wishlist = self.wishdict
        setting = self.setting

        itad = setting.get('itad', {})
        net = setting.get('net', {})

        proxy = net.get('proxy', None)
        token = itad.get('token')
        region = itad.get('region', 'cn')
        country = itad.get('country', 'CN')

        ids = list(wishlist.keys())
        self.logger.info('开始获取游戏ID,第一次耗时会比较久')
        plaindict = await get_plains(ids, token, True, proxy)
        self.logger.info(f'游戏ID读取完毕,共{len(plaindict)}条')

        plains = list(plaindict.values())
        self.logger.info('开始获取游戏价格信息,可能会比较久')
        current_dict = await get_current_price(plains, token, region, country, proxy)
        lowest_dict = await get_lowest_price(plains, token, region, country, proxy)
        print('')
        self.logger.info('整理游戏价格数据')
        for key in wishlist.keys():
            try:
                plain = plaindict[key]
            except KeyError:
                self.logger.debug(f'未找到ID为{key}的plain,已忽略')
                continue

            obj = wishlist[key]

            if not obj['free']:
                try:
                    p_now, p_old, p_cut = current_dict[plain]
                except KeyError:
                    # 没有当前价格数据
                    p_now, p_old, p_cut = -1, -1, 0
                try:
                    p_low, p_low_cut, p_low_time = lowest_dict[plain]
                except KeyError:
                    # 没有史低价格数据
                    p_low, p_low_cut, p_low_time = -1, 0, 0
            else:
                # 免费游戏
                p_now, p_old, p_cut = 0, 0, 0
                p_low, p_low_cut, p_low_time = 0, 0, 0

            obj['price'] = {
                'current': p_now,
                'origin': p_old,
                'current_cut': p_cut,
                'lowest': p_low,
                'low_cut': p_low_cut,
                'low_time': p_low_time,
                'is_lowest': is_lowest(p_old, p_now, p_low, p_cut)
            }
            # obj['price_current'] = p_now
            # obj['price_origion'] = p_old
            # obj['price_cut'] = p_cut
            # obj['price_lowest'] = p_low
            # obj['price_low_cut'] = p_low_cut
            # obj['price_low_time'] = p_low_time
        self.logger.info('价格数据整理完成')

    async def add_addition(self):
        '''
        获取游戏附加信息
        '''
        wishdict = self.wishdict
        setting = self.setting
        net = setting.get('net', {})
        proxy = net.get('proxy', None)

        ids = list(wishdict.keys())
        errors = 0
        if setting['keylol']['enable']:
            self.logger.info('使用Keylol模块获取附加信息,可能会比较久')
            additiondict = await get_games_tags(ids)
            for key in wishdict.keys():
                try:
                    obj = wishdict[key]
                    add = additiondict[key]
                    # obj['tags'] = add['tags']
                    obj['card'] = add['card']
                    # obj['name_cn'] = add['name_cn']
                except KeyError:
                    errors += 1
                    self.logger.debug(f'ID {key}处理失败')
        else:
            self.logger.info('使用ITAD模块获取附加信息,可能会比较久')
            token = setting['itad']['token']
            plaindict = await get_plains(ids, token, True, proxy)
            self.logger.info(f'ID读取完毕,共{len(plaindict)}条')
            plains = list(plaindict.values())
            additiondict = await get_base_info(plains, token, proxy)
            for key in wishdict.keys():
                try:
                    plain = plaindict[key]
                    obj = wishdict[key]
                    obj['card'] = additiondict[plain]
                    # obj['tags'] = None
                    # obj['name_cn'] = None
                except KeyError:
                    errors += 1
                    self.logger.debug(f'ID {key}处理失败')
        print('')
        self.logger.debug(f'总计{errors}个错误')
        self.logger.info('附加信息读取完成')

    def filter(self):
        '''
        按照配置过滤愿望单
        '''
        wishdict = self.wishdict
        filter = self.setting['filter']
        f = Filter(filter)
        wishdict = {k: v for k, v in wishdict.items() if f.filter(v)}
        self.logger.info(f'过滤后共有{len(wishdict)}个游戏')
        self.wishdict = wishdict

    def sort(self):
        '''
        按照配置过滤愿望单
        '''
        wishdict = self.wishdict
        sort = self.setting['sort']
        self.index = get_index(wishdict, sort)

    def output(self):
        '''
        按照配置输出到文件
        '''
        wishdict = self.wishdict
        index = self.index
        symbol = self.setting['itad']['currency_symbol']
        setting = self.setting['output']

        cmd = setting.get('console', False)
        md = setting.get('markdown', False)
        xlsx = setting.get('xlsx', False)
        bbc = setting.get('bbcode', False)
        jsn = setting.get('json', False)

        if not index:
            index = wishdict.keys()

        self.logger.info('开始输出')
        if md:
            try:
                markdown.handler(wishdict, index, symbol)
            except Exception as e:
                self.logger.error(f'遇到错误: {e}')
        if xlsx:
            try:
                excel.handler(wishdict, index, symbol)
            except Exception as e:
                self.logger.error(f'遇到错误: {e}')
        if bbc:
            try:
                bbcode.handler(wishdict, index, symbol)
            except Exception as e:
                self.logger.error(f'遇到错误: {e}')
        if cmd:
            try:
                self.logger.warning('因为打包程序有问题,暂时禁用控制台输出的功能')
                # console.handler(wishdict, index, symbol)
            except Exception as e:
                self.logger.error(f'遇到错误: {e}')
        if jsn:
            try:
                json.handler(wishdict, index, symbol)
            except Exception as e:
                self.logger.error(f'遇到错误: {e}')

        self.logger.info('输出完成')
