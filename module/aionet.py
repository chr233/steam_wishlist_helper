# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-07-11 12:25:45
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-08 14:41:47
# @Description  : 网络请求模块
'''
import re
import json
import asyncio

from httpx import Response, AsyncClient

from .log import get_logger
from .static import TREAD_CD

logger = get_logger('Net')


async def adv_http_get(client: AsyncClient, url: str, params: dict = None,
                       headers: dict = None, retrys: int = 3) -> Response:
    '''
    出错自动重试的请求器

    参数:
        client: httpx对象
        url: url
        params: params
        headers: headers
        [retrys]: 重试次数,默认为3
    返回:
        Response: 请求结果
    '''
    for _ in range(0, retrys):
        try:
            resp = await client.get(url=url, params=params, headers=headers)
            print('.', end='')
            await asyncio.sleep(TREAD_CD)
            return (resp)
        except Exception:
            logger.debug('网络错误,暂停10秒')
            await asyncio.sleep(10)
    logger.error('网络错误,请求失败')
    return (None)


async def adv_http_get_keylol(client: AsyncClient, url: str, params: dict = None,
                              headers: dict = None, retrys: int = 3) -> Response:
    '''
    出错自动重试的请求器

    参数:
        client: httpx对象
        url: url
        params: params
        headers: headers
        [retrys]: 重试次数,默认为3
    返回:
        Response: 请求结果
    '''
    for _ in range(0, retrys):
        try:
            resp = await client.get(url=url, params=params, headers=headers)
            print('.', end='')
            pattern = re.compile(r'(\{.+\})', re.MULTILINE)
            matchobj = pattern.search(resp.text)
            jd = json.loads(matchobj.group(1))
            await asyncio.sleep(TREAD_CD)
            return (jd)
        except Exception as e:
            logger.debug(f'网络错误,暂停30秒 {e}')
            await asyncio.sleep(30)
    logger.error('网络错误,请求失败')
    return {}