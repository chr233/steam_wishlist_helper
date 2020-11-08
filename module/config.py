# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-06-30 17:32:56
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-08 15:26:33
# @Description  : 读取并验证配置
'''

import toml

from os import getcwd, path

from .log import get_logger

logger = get_logger('Config')
default_path = path.join(getcwd(), 'config.toml')


def get_config(path: str = default_path) -> dict:
    '''读取并验证配置

    参数:
        [path]:配置文件路径,默认为config.toml
    返回:
        dict:验证过的配置字典,如果读取出错则返回None
    '''
    try:
        logger.info('开始读取配置')
        raw_cfg = dict(toml.load(path))
        cfg = verify_config(raw_cfg)
        logger.info('配置验证通过')
        return (cfg)

    except FileNotFoundError:
        logger.error(f'配置文件[{path}]不存在')
        with open(path, 'w+', encoding='utf-8') as f:
            toml.dump(verify_config({}), f)
        logger.error('已生成默认配置,请重新运行程序')

    except ValueError as e:
        logger.error(f'配置文件验证失败[{e}]')


def verify_config(cfg: dict) -> dict:
    '''验证配置

    参数:
        cfg:配置字典
    返回:
        dict:验证过的配置字典,剔除错误的和不必要的项目
    '''
    vcfg = {'itad': {}, 'keylol': {}, 'steam': {},
            'output': {}, 'auto': {}}

    itad = cfg.get('itad', {})
    token = itad.get('token', '')
    region = itad.get('region', 'cn')
    country = itad.get('country', 'CN')
    symbol = itad.get('currency_symbol', '¥')

    if not token and cfg:
        raise ValueError('未设置API token,可以自行申请或者使用文档中的公共token')

    vcfg['itad'] = {
        'token': token,
        'region': region,
        'country': country,
        'currency_symbol': symbol
    }

    keylol = cfg.get('keylol', {})
    enable = bool(keylol.get('enable', True))

    vcfg['keylol'] = {
        'enable': enable
    }

    steam = cfg.get('steam', {})
    language = steam.get('language', 'schinese')
    small_game_pic = bool(steam.get('small_game_pic', True))
    proxy = steam.get('proxy', None)

    vcfg['steam'] = {'language': language,
                     'small_game_pic': small_game_pic,
                     'proxy': proxy}

    output = cfg.get('output', {})
    console = bool(output.get('console', True))
    markdown = bool(output.get('markdown', False))
    xlsx = bool(output.get('xlsx', True))
    bbcode = bool(output.get('bbcode', False))

    vcfg['output'] = {'console': console,
                      'markdown': markdown,
                      'xlsx': xlsx,
                      'bbcode': bbcode}

    auto = cfg.get('auto', {})
    steamid = auto.get('steamid', None)
    if (steamid and not isinstance(steamid, list)):
        steamid = [steamid]

    vsteamid = []
    if steamid:
        for i in range(0, len(steamid)):
            try:
                vsteamid.append(int(steamid[i]))
            except ValueError:
                logger.warning(f'错误的steamid: [{steamid[i]}]')

    vcfg['auto'] = {'steamid': vsteamid}
    return (vcfg)
