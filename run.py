# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-11-01 00:00:47
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-09 19:49:36
# @Description  : 启动入口
'''

import asyncio

from module.config import get_config
from module.crawer import crawer
from module.log import get_logger
from module.version import check_update

logger = get_logger('Main')


async def main():
    cfg = get_config()
    if cfg:
        steamid = cfg['auto']['steamid'] or [input('请输入64位steam ID: ')]
        vc, vl, i, u = await check_update(cfg)
        c = crawer(cfg, steamid)
        await c.start()

        # 检查脚本更新
        if (vc == vl):
            logger.info(f'已经是最新版本 [{vc}]')
        elif (vc > vl):
            logger.info(f'已经是最新版本 [{vc}<-{vl}]')
        else:
            logger.info((f'[*] 脚本有更新 [{vc}->{vl}]'
                         f'{i}'
                         f'{u}'))
        try:
            if (cfg['other']['wait_screen']):
                input('运行结束,按回车键退出……')
            else:
                print('运行结束,程序退出')
        except KeyboardInterrupt:
            pass
    else:
        logger.info('读取配置文件失败')
        input('运行结束,按回车键退出……')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
