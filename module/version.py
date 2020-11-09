# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-11-08 10:11:20
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-09 19:50:21
# @Description  : 版本管理
'''

from re import split
from httpx import AsyncClient
from typing import Tuple

from .log import get_logger
from .aionet import adv_http_get
from .static import SCRIPT_VERSION, URLs

logger = get_logger('Version')


async def check_update(setting: dict) -> Tuple[str, str, str, str]:
    logger.info('正在后台检查更新')
    net = setting.get('net', {})
    proxy = net.get('proxy', None)
    async with AsyncClient(proxies=proxy) as client:
        url = URLs.Github_Releases_API
        resp = await adv_http_get(client=client, url=url)
        current_version = float(SCRIPT_VERSION)
        if resp:
            try:
                jd = resp.json()
                latest_version = float(str(jd['tag_name']))
                update_info = jd['body']
                download_url = jd['assets'][0]['browser_download_url']
                if (current_version == latest_version):
                    logger.debug(f'当前为最新版本 [{current_version}]')
                elif (current_version > latest_version):
                    logger.debug(
                        f'当前版本号比发行版高 [{current_version}<-{latest_version}]')
                else:
                    logger.debug(
                        f'脚本有更新 [{current_version}->{latest_version}]')
                return ((current_version, latest_version, update_info, download_url))
            except Exception:
                logger.debug('检查最新版本出错')
                return ((current_version, current_version, '检查更新出错', URLs.Github_Releases))
        else:
            logger.debug('检查最新版本出错')
            return ((current_version, current_version, '检查更新出错', URLs.Github_Releases))
