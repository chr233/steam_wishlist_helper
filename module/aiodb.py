# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-07-08 10:42:53
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-07 17:48:23
# @Description  : 读写缓存数据库
'''

from .log import get_logger
from aiosqlite import DatabaseError, OperationalError, NotSupportedError,Connection

logger = get_logger('Db')


async def init_db(conn: Connection, drop_if_exist: bool = False):
    '''
    初始化数据库

    参数:
        conn: 数据库连接对象
        drop_if_exit: 如果数据表已存在是否先删表
    '''
    sql = ('PRAGMA foreign_keys = false;'
           f'{"""DROP TABLE IF EXISTS "plains";""" if drop_if_exist else ""}'
           'CREATE TABLE "plains" ('
           '"id" INTEGER NOT NULL COLLATE BINARY,'
           '"plain" TEXT NOT NULL,'
           'PRIMARY KEY ("id"));'
           'CREATE UNIQUE INDEX "id" ON "plains" ("id" COLLATE BINARY ASC);'
           'PRAGMA foreign_keys = true;')
    if drop_if_exist:
        logger.warning('即将清除原数据表')
    else:
        logger.warning('即将初始化数据库')
    try:
        await conn.executescript(sql)
        await conn.commit()
        logger.warning('初始化数据库完成')
    except (DatabaseError, OperationalError, NotSupportedError) as e:
        logger.warning(f'数据库读写失败 - {e}')


async def set_plain(conn: Connection, id: int, plain: str):
    '''
    向数据库写入id和plain

    参数:
        conn: 数据库连接对象
        id: appid或者subid,需为数字
        plain: itad使用的游戏标识
    '''
    sql = 'INSERT INTO "main"."plains"("id", "plain") VALUES (?,?);'
    try:
        await conn.execute(sql, (str(id), plain))
        await conn.commit()
    except (DatabaseError, OperationalError, NotSupportedError) as e:
        logger.warning(f'操作数据库失败 {e}')


async def get_plain(conn: Connection, id: int) -> str:
    '''
    使用id向数据库查询plain

    参数:
        conn: 数据库连接对象
        id: appid或者subid,需为数字
    '''
    sql = 'SELECT "plain" From "main"."plains" WHERE "id" = ?;'
    try:
        cur = await conn.cursor()
        await cur.execute(sql, (str(id),))
        result = await cur.fetchone()
        if result:
            plain, = result
        else:
            plain = None
        return (plain)
    except (DatabaseError, OperationalError, NotSupportedError) as e:
        logger.warning(f'操作数据库失败 {e}')


async def del_plain(conn: Connection, id: int) -> str:
    '''
    删除指定id,仅供测试
    
    参数:
        conn: 数据库连接对象
        id: appid或者subid,需为数字
    '''
    sql = 'DELETE FROM "main"."plains" WHERE "id" = ?;'
    try:
        await conn.execute(sql, (str(id),))
        await conn.commit()
    except (DatabaseError, OperationalError, NotSupportedError) as e:
        logger.warning(f'操作数据库失败 {e}')
