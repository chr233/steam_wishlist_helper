# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-07-08 19:48:26
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-08 12:27:58
# @Description  : 对接ITAD的API【异步】
'''

import asyncio
import aiosqlite

from os import path
from httpx import AsyncClient
from json import JSONDecodeError

from .aiodb import get_plain, set_plain, init_db
from .log import get_logger
from .aionet import adv_http_get
from .static import URLs, DB_NAME

logger = get_logger('ITAD')


async def get_plains(ids: list, token: str, use_cache: bool = True) -> dict:
    '''
    把appid或subid转换成IsThereAnyDeal使用的plainid

    参数：
        ids: appid列表,例如[730]
        token: ITAD的API token
        [use_cache]: 是否使用缓存,开启后优先读取本地数据库,默认为True

    返回：
        dict: {id:plain} (如果id有误则返回None)
    '''
    if not path.exists(DB_NAME):
        logger.warning('缓存数据库不存在,创建data.db')
        async with aiosqlite.connect(DB_NAME) as conn:
            await init_db(conn, True)

    params = {'key': token, 'shop': 'steam', 'ids': ''}
    id2pdict = {}
    async with asyncio.Semaphore(3):  # 最大并发数
        if use_cache:  # 如果启用缓存则优先从本地读取plain
            async with aiosqlite.connect(DB_NAME) as conn:
                ncache = []
                for id_ in ids:
                    plain = await get_plain(conn, id_)
                    if not plain:
                        ncache.append(id_)
                    else:
                        id2pdict[id_] = plain
        else:
            ncache = ids
        async with AsyncClient() as client:
            max = len(ncache)
            if max:
                tasks = set()
                for i in range(0, max, 30):
                    part = ncache[i:i+30]
                    tasks.add(asyncio.create_task(
                        _get_plain(client, params, part)))
                await asyncio.wait(tasks)

                for task in tasks:
                    dic = task.result()
                    if use_cache:  # 如果启用缓存则将结果写入数据库
                        async with aiosqlite.connect(DB_NAME) as conn:
                            for key in dic.keys():
                                if dic[key]:
                                    await set_plain(conn, key, dic[key])
                    id2pdict.update(dic)
    return (id2pdict)


async def _get_plain(client: AsyncClient, params: dict, ids: list) -> str:
    '''
    把appid或subid转换成IsThereAnyDeal使用的plainid

    参数：
        client: httpx Client对象
        params: 参考get_plain里的用法
    返回：
        dict: {id:plain} (如果id有误则返回None)
    '''
    url = URLs.ITAD_ID_To_Plain
    params['ids'] = ','.join([f'app/{x}' for x in ids])
    resp = await adv_http_get(client=client, url=url, params=params)
    result = {}
    if resp:
        try:
            data = resp.json().get('data', {})
        except (JSONDecodeError, AttributeError) as e:
            logger.error(f'解析json出错 - {e}')
            data = {}
        for id_ in ids:
            plain = data.get(f'app/{id_}', None)
            if not plain:
                logger.warning(f'读取App{id_}出错,忽略该App')
            else:
                result[id_] = plain
    return (result)


async def get_current_price(plains: list, token: str, region: str, country: str) -> dict:
    '''
    使用plainid获取当前价格

    参数：
        plains: plain列表,例如['counterstrikeglobaloffensive']
        token: ITAD的API token
        region: 地区
        country: 国家
    返回：
        dict: 价格字典,以plain为键名,每个键是(现价,原价,折扣)
    '''
    params = {'key': token,  'plains': '', 'region': region,
              'country': country, 'shops': 'steam'}
    pricedict = {}
    if plains:
        async with asyncio.Semaphore(3):  # 最大并发数
            async with AsyncClient() as client:
                max = len(plains)
                tasks = set()
                for i in range(0, max, 5):
                    part = plains[i:i+5]
                    tasks.add(asyncio.create_task(
                        _get_current_price(client, params, part)))
                await asyncio.wait(tasks)
        for task in tasks:
            dic = task.result()
            pricedict.update(dic)
    return (pricedict)


async def _get_current_price(client: AsyncClient, params: dict, plains: list) -> dict:
    '''
    获取Steam商店当前价格

    参数：
        client: httpx Client对象
        params: 参考get_current_price里的用法
    返回：
        dict: 价格字典,以plain为键名,每个键是(现价,原价,折扣)
    '''
    url = URLs.ITAD_Get_Current_Prices
    params['plains'] = ','.join(plains)
    resp = await adv_http_get(client=client, url=url, params=params)
    pricedict = {}
    if resp:
        try:
            data = resp.json().get('data', {})
        except (JSONDecodeError, AttributeError):
            logger.error(f'json解析失败')
            data = {}
        for plain in data.keys():
            d = data[plain].get('list', None)
            if len(d) > 1:
                logger.debug(f'{plain} {d}')
            if d:
                p_new = d[0]['price_new']
                p_old = d[0]['price_old']
                p_cut = d[0]['price_cut']
            else:
                # 未发售游戏,没有价格,标记为-1
                p_new, p_old, p_cut = -1, -1, 0
            pricedict[plain] = (p_new, p_old, p_cut)
    return (pricedict)


async def get_lowest_price(plains: list, token: str, region: str, country: str) -> dict:
    '''
    获取Steam商店史低价格

    参数:
        plains: plain列表,例如['counterstrikeglobaloffensive']
        token: ITAD的API token
        region: 地区
        country: 国家
    返回:
        dict: 价格字典,以plain为键名,每个键是(史低,史低折扣,史低时间)
    '''
    params = {'key': token,  'plains': '', 'region': region,
              'country': country, 'shops': 'steam'}
    pricedict = {}
    if plains:
        async with asyncio.Semaphore(3):  # 最大并发数
            async with AsyncClient() as client:
                max = len(plains)
                tasks = set()
                for i in range(0, max, 5):
                    part = plains[i:i+5]
                    tasks.add(asyncio.create_task(
                        _get_lowest_price(client, params, part)))
                await asyncio.wait(tasks)
        for task in tasks:
            dic = task.result()
            pricedict.update(dic)
    return (pricedict)


async def _get_lowest_price(client: AsyncClient, params: dict, plains: list) -> dict:
    '''
    获取Steam商店史低价格

    参数：
        client: httpx Client对象
        params: 参考get_lowest_price里的用法
        plains: plains列表
    返回：
        dict: 价格字典,以plain为键名,每个键是(史低,史低折扣,史低时间)
    '''
    url = URLs.ITAD_Get_Lowest_Prices
    params['plains'] = ','.join(plains)
    resp = await adv_http_get(client=client, url=url, params=params)
    pricedict = {}
    if resp:
        try:
            data = resp.json().get('data', {})
        except (JSONDecodeError, AttributeError):
            logger.error(f'json解析失败')
            data = {}
        for plain in data.keys():
            d = data[plain]
            if 'price' in d:
                p_low = d['price']
                p_cut = d['cut']
                p_time = d['added']
            else:
                # 未发售游戏,没有价格,标记为-1
                p_low, p_cut, p_time = -1, 0, 0
            pricedict[plain] = (p_low, p_cut, p_time)
    return (pricedict)


async def get_base_info(plains: list, token: str) -> dict:
    '''
    获取Steam商店游戏信息【只能获取2个属性,不建议使用】

    参数:
        plains: plain列表,例如['counterstrikeglobaloffensive']
        token: ITAD的API token
    返回:
        dict: 游戏信息字典,(有成就,有卡牌)
    '''
    params = {'key': token,  'plains': ''}
    infodict = {}
    if plains:
        async with asyncio.Semaphore(3):  # 最大并发数
            async with AsyncClient() as client:
                max = len(plains)
                tasks = set()
                for i in range(0, max, 5):
                    part = plains[i:i+5]
                    tasks.add(asyncio.create_task(
                        _get_base_info(client, params, part)))
                await asyncio.wait(tasks)
        for task in tasks:
            dic = task.result()
            infodict.update(dic)
    return (infodict)


async def _get_base_info(client: AsyncClient, params: dict, plains: list) -> dict:
    '''获取Steam商店史低价格
    参数：
        client: httpx Client对象
        params: 参考get_base_info里的用法
        plains: plains列表
    返回：
        dict: 游戏信息字典
    '''
    url = URLs.ITAD_Get_Game_Info
    params['plains'] = ','.join(plains)
    resp = await adv_http_get(client=client, url=url, params=params)
    infodict = {}
    if resp:
        try:
            data = resp.json().get('data', {})
        except (JSONDecodeError, AttributeError):
            logger.error(f'json解析失败')
            data = {}
        for plain in data.keys():
            d = data[plain]
            has_achi = d.get('achievements', False)
            has_card = d.get('trading_cards', False)
            infodict[plain] = (has_card, has_achi)
    return (infodict)
