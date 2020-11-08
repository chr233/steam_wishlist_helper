# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-06-30 05:08:57
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-08 12:30:57
# @Description  : 对接Keylol的API【异步】
'''

import asyncio
from httpx import AsyncClient

from .log import get_logger
from .static import URLs
from .aionet import adv_http_get_keylol


logger = get_logger('Keylol')


async def get_games_tags(appids: list) -> dict:
    '''
    异步读取Steam愿望单

    参数:
        appids: appid列表
    返回：
        dict: 游戏信息字典
    '''
    gameinfo = {}
    if appids:
        async with asyncio.Semaphore(2):  # 最大并发数
            async with AsyncClient() as client:
                tasks = {
                    asyncio.create_task(_get_game_tags(client=client, appid=i)) for i in appids
                }
                await asyncio.wait(tasks)
        for task in tasks:
            gameinfo.update(task.result())
    return (gameinfo)


async def _get_game_tags(client: AsyncClient, appid: int) -> dict:
    '''
    其乐API,读取steam游戏信息

    参数:
        appid: appid
    返回:
        dict: 包含游戏附加信息的dict
    '''
    url = URLs.Keylol_Get_Game_Info % appid
    async with AsyncClient() as client:
        jd = await adv_http_get_keylol(client=client,
                                       url=url,
                                       retrys=3)
    result = {}
    if jd:
        result[appid] = {
            'tags': set(jd.get('tags', []) + jd.get('genre', [])),
            # 'categories': [(int(x[0]), x[1])for x in raw.get('categories', [])],
            'has_card': len(jd.get('card', [])) > 0,
            'description': jd.get('description', '')}
    return (result)
