# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-11-08 10:11:20
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-26 16:02:20
# @Description  : 版本管理
'''

from httpx import AsyncClient
from typing import Tuple

from .log import get_logger
from .aionet import adv_http_get
from .static import SCRIPT_VERSION, URLs

logger = get_logger('Version')


async def check_update(setting: dict):
    '''
    检查脚本更新
    '''
    vc, vl, i, u = await __check_update(setting)
    # 检查脚本更新
    if (vc == vl):
        logger.info(f'已经是最新版本,当前版本 [{vc}]')
    elif (vc > vl):
        logger.info(f'已经是最新版本,当前版本 [{vc}] , 最新发布版本 [{vl}]')
    else:
        print('\n'*2)
        logger.info((f'[*] 脚本有更新,最新发布版本 [{vl}]\n'
                     '更新内容:\n'
                     f'{i}\n'
                     f'{u}'))
        print('\n'*2)


async def __check_update(setting: dict) -> Tuple[str, str, str, str]:
    '''
    检查脚本版本
    '''
    logger.debug('正在后台检查更新')
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
