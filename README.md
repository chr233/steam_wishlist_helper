
# Steam Wishlist Helper

[![Codacy Badge][b1]][b2] [![Release][b5]][b4] [![Download][b3]][b4] [![License][b7]][b6]

结合ITAD的价格查询功能, 生成一份自己的游戏折扣列表

需要Python3.8及以上

> [蓝奏云镜像][2] 密码:cg84

## 使用方法

* 从[发布页][0]或者[蓝奏云][2] (密码:cg84) 下载最新版本并解压
* pip install -r requirements.txt
* 将 example.config.toml 重命名为 config.toml
* 修改 config.toml , 填入自己的API Token([申请地址][1])
* python3 run.py

## TODO

- [x] 加入过滤器
- [ ] 加入排序功能
- [ ] 加一个GUI

[b1]:https://app.codacy.com/project/badge/Grade/d295529050004976aa50252d61eda98e
[b2]:https://www.codacy.com/gh/chr233/steam_wishlist_helper/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=chr233/steam_wishlist_helper&amp;utm_campaign=Badge_Grade
[b3]: https://img.shields.io/github/downloads/chr233/steam_wishlist_helper/total
[b4]: https://github.com/chr233/steam_wishlist_helper/releases
[b5]: https://img.shields.io/github/v/release/chr233/steam_wishlist_helper
[b6]: https://github.com/chr233/steam_wishlist_helper/blob/master/license
[b7]: https://img.shields.io/github/license/chr233/steam_wishlist_helper
[0]: https://github.com/chr233/steam_wishlist_helper/releases
[1]: https://new.isthereanydeal.com/apps/mine/
[2]: https://wws.lanzous.com/b01nqwxta
