# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-06-30 17:32:56
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-14 14:13:40
# @Description  : 读取并验证配置
'''

from os import getcwd, path

import toml

from .log import get_logger
from .utils import dint, fint, fbool, flist
from .static import SORT_TYPE

logger = get_logger('Config')
default_path = path.join(getcwd(), 'config.toml')


def get_config(path: str = default_path) -> dict:
    '''
    读取并验证配置

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
    '''
    验证配置

    参数:
        cfg:配置字典
    返回:
        dict:验证过的配置字典,剔除错误的和不必要的项目
    '''
    auto = __verify_auto(cfg.get('auto', {}))

    other = __verify_other(cfg.get('other', {}))

    itad = __verify_itad(cfg.get('itad', {}))
    if not itad['token'] and cfg:
        raise ValueError('未设置API token,可以自行申请或者使用文档中的公共token')

    keylol = __verify_keylol(cfg.get('keylol', {}))

    steam = __verify_steam(cfg.get('steam', {}))

    net = __verify_net(cfg.get('net', {}))

    output = __verify_output(cfg.get('output', {}))

    sort = __verify_sort(cfg.get('sort', {}))

    filter = __verify_filter(cfg.get('filter', {}))

    vcfg = {'auto': auto, 'other': other, 'itad': itad,
            'keylol': keylol, 'steam': steam, 'net': net,
            'output': output, 'sort': sort, 'filter': filter}

    return (vcfg)


def __verify_auto(auto: dict) -> dict:
    '''
    验证auto节
    '''
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
    auto = {'steamid': steamid}
    return (auto)


def __verify_other(other: dict) -> dict:
    '''
    验证other节
    '''
    wait_screen = bool(other.get('wait_screen', True))
    other = {'wait_screen': wait_screen}
    return (other)


def __verify_itad(itad: dict) -> dict:
    '''
    验证itad节
    '''
    token = itad.get('token', '')
    region = itad.get('region', 'cn')
    country = itad.get('country', 'CN')
    symbol = itad.get('currency_symbol', '¥')
    itad = {'token': token,
            'region': region,
            'country': country,
            'currency_symbol': symbol}
    return (itad)


def __verify_keylol(keylol: dict) -> dict:
    '''
    验证keylol节
    '''
    enable = bool(keylol.get('enable', True))
    keylol = {'enable': enable}
    return (keylol)


def __verify_steam(steam: dict) -> dict:
    '''
    验证steam节
    '''
    language = steam.get('language', 'schinese')
    small_game_pic = bool(steam.get('small_game_pic', True))
    steam = {'language': language,
             'small_game_pic': small_game_pic}
    return (steam)


def __verify_net(net: dict) -> dict:
    '''
    验证net节
    '''
    proxy = net.get('proxy', None)
    p = {"http://": proxy, "https://": proxy} if proxy else None
    net = {'proxy': p}
    return (net)


def __verify_output(output: dict) -> dict:
    '''
    验证output节
    '''
    console = bool(output.get('console', False))
    markdown = bool(output.get('markdown', True))
    xlsx = bool(output.get('xlsx', True))
    bbcode = bool(output.get('bbcode', False))
    json = bool(output.get('json', False))

    output = {'console': console, 'markdown': markdown,
              'xlsx': xlsx, 'bbcode': bbcode, 'json': json}
    return (output)


def __verify_sort(sort: dict) -> dict:
    ''' 
    验证sort节
    '''
    index = dint(sort.get('index', 0), 0)
    if(abs(index) > SORT_TYPE):
        index = 0
        logger.warning(f'[filter]节 index 设置有误 (index = {index})')
    sort = {'index': index}
    return (sort)


def __verify_filter(filter: dict) -> dict:
    ''' 
    验证filter节
    '''
    price_set = fbool(filter.get('price_set', -1))
    price_noset = fbool(filter.get('price_noset', -1))
    price_free = fbool(filter.get('price_free', -1))
    price_higher = fint(filter.get('price_higher', -1), 0)
    price_lower = fint(filter.get('price_lower', -1), 0)

    discount_higher = fint(filter.get('discount_higher', -1), 100)
    discount_lower = fint(filter.get('discount_lower', -1), 100)
    discount_not_lowest = fbool(filter.get('discount_not_lowest', -1))
    discount_is_lowest = fbool(filter.get('discount_is_lowest', -1))
    discount_almost_lowest = fbool(filter.get('discount_almost_lowest', -1))

    review_score_higher = fint(filter.get('review_score_higher', -1), 9)
    review_score_lower = fint(filter.get('review_score_lower', -1), 9)
    review_percent_higher = fint(filter.get('review_percent_higher', -1), 100)
    review_percent_lower = fint(filter.get('review_percent_lower', -1), 100)
    review_count_higher = fint(filter.get('review_count_higher', -1), 0)
    review_count_lower = fint(filter.get('review_count_lower', -1), 0)

    platform_windows = fbool(filter.get('platform_windows', -1))
    platform_mac = fbool(filter.get('platform_mac', -1))
    platform_linux = fbool(filter.get('platform_linux', -1))

    tags_include = flist(filter.get('tags_include', -1))
    tags_exclude = flist(filter.get('tags_exclude', -1))

    filter = {
        'price_set': price_set,
        'price_noset': price_noset,
        'price_free': price_free,
        'price_higher': price_higher,
        'price_lower': price_lower,

        'discount_higher': discount_higher,
        'discount_lower': discount_lower,
        'discount_not_lowest': discount_not_lowest,
        'discount_is_lowest': discount_is_lowest,
        'discount_almost_lowest': discount_almost_lowest,

        'review_score_higher': review_score_higher,
        'review_score_lower': review_score_lower,
        'review_percent_higher': review_percent_higher,
        'review_percent_lower': review_percent_lower,
        'review_count_higher': review_count_higher,
        'review_count_lower': review_count_lower,

        'platform_windows': platform_windows,
        'platform_mac': platform_mac,
        'platform_linux': platform_linux,

        'tags_include': tags_include,
        'tags_exclude': tags_exclude
    }
    return (filter)
