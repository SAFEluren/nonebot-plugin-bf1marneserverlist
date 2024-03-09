import json

import httpx
from nonebot import get_plugin_config
from nonebot import on_command
from nonebot import require
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata

require('nonebot_plugin_localstore')
import nonebot_plugin_localstore as store

from .config import Config

__plugin_meta__ = PluginMetadata(
    name='战地1-马恩私人服务器服务器查询',
    description='Onebot 战地1 马恩私人服务器服务器查询插件',
    usage='''
    /marne : 获取当前群聊绑定的服务器的信息
    /marne bind : 仅群主、管理员、机器人SUPERUSER 可用，绑定服务器到当前群聊
    /marne mods : 获取当前群聊绑定的服务器的模组信息
    /marne player : 获取当前群聊绑定的服务器的在线玩家列表
    
    ''',

    type='application',
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage='https://github.com/SAFEluren/nonebot-plugin-bf1marneserverlist',
    # 发布必填。

    config=Config,
    # 插件配置项类，如无需配置可不填写。

    supported_adapters={'~onebot.v11'},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

plugin_config = get_plugin_config(Config)
data_dir = store.get_data_dir('bf1marneserverlist')

marne_url = plugin_config.marne_url


async def is_enable() -> bool:
    return plugin_config.marne_plugin_enabled


MARNE_MAIN = on_command('marne', aliases={'查服'})
MARNE_MODS = on_command('marne mods', aliases={'查服 模组'})
MARNE_PLST = on_command('marne player', aliases={'查服 玩家'})
MARNE_MAPS = on_command('marne map', aliases={'查服 地图'})
MARNE_BIND = on_command('marne bind', permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER)


async def request_marneapi(marne_serverid):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{marne_url}api/srvlst/{marne_serverid}')
            content = response.text
            if content is not None and content != '[]':
                return content
            else:
                print('Response content is None')
                await MARNE_MAIN.send('无法获取到服务器数据，请检查输入的马恩服务器ID是否正确，或服务器当前未开启。',reply_message=True)
                return None

    except (httpx.HTTPStatusError, httpx.ConnectTimeout) as e:
        print(f'HTTP error occurred: {e}')


@MARNE_MAIN.handle()
# async def marne_info(event: GroupMessageEvent):
async def _info(event: GroupMessageEvent):
    session = event.group_id
    try:
        with open(data_dir / f'{session}.json', 'r', encoding='utf-8') as f:
            group = json.load(f)
    except FileNotFoundError:
        await MARNE_MAIN.send('请先绑定服务器ID.')
        return
    serverID = group['id']
    results = await request_marneapi(serverID)

    result = json.loads(results)
    server_ID = result['id']
    server_name = result['name']
    server_description = result['description']
    server_region = result['region']
    server_country = result['country']
    server_map = result['map']
    server_mode = result['mode']
    server_currentPlayers = result['currentPlayers']
    server_maxPlayers = result['maxPlayers']

    with open(data_dir / f'{session}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    msg = Message([MessageSegment.text(f'查询成功')])
    msg.append(f'\n服务器ID: {server_ID}')
    msg.append(f'\n服务器名字: {server_name}')
    msg.append(f'\n服务器简介: {server_description}')
    msg.append(f'\n服务器区域: {server_region} - {server_country}')
    msg.append(f'\n当前地图: {server_map}')
    msg.append(f'\n游戏模式: {server_mode}')
    msg.append(f'\n当前人数: {server_currentPlayers} / {server_maxPlayers}')

    await MARNE_BIND.finish(msg)


@MARNE_MODS.handle()
# async def marne_info(event: GroupMessageEvent):
async def _mods(event: GroupMessageEvent):
    session = event.group_id

    try:
        with open(data_dir / f'{session}.json', 'r', encoding='utf-8') as f:
            group = json.load(f)
    except FileNotFoundError:
        await MARNE_MODS.send('请先绑定服务器ID.',reply_message=True)
        return
    serverID = group['id']
    results = await request_marneapi(serverID)
    result = json.loads(results)
    server_ID = result['id']
    server_name = result['name']
    server_description = result['description']
    server_region = result['region']
    server_country = result['country']

    with open(data_dir / f'{session}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    # 定义键值对的映射关系
    key_mapping = {
        'name': '名称',
        'version': '版本',
        'category': '分类',
        'link': '链接'
    }
    # 访问'ModList'键节点下所有键值对并转换为消息
    mod_list = result['modList']
    msg = Message([MessageSegment.text(f'查询成功')])
    msg.append(f'\n服务器ID: {server_ID}')
    msg.append(f'\n服务器名字: {server_name}')
    msg.append(f'\n服务器简介: {server_description}')
    msg.append(f'\n服务器区域: {server_region} - {server_country}')
    msg.append(f'\n---------- MOD信息 ----------')

    if len(mod_list) > 0:
        for index, mod in enumerate(result['modList'], start=1):
            mod_info = []
            for key in ['name', 'version', 'category', 'link']:
                value = mod.get(key)
                if value:
                    mod_info.append(f'\n{key_mapping.get(key, key)}: {value}')
            msg.append(''.join(mod_info))
            if index < len(result['modList']):
                msg.append(f'\n---------- 以上是第{index}个MOD ----------')
    else:
        msg = Message([MessageSegment.text('服务器无 MOD')])

    await MARNE_MODS.finish(msg,reply_message=True)


@MARNE_PLST.handle()
# async def marne_info(event: GroupMessageEvent):
async def _players(event: GroupMessageEvent):
    session = event.group_id

    try:
        with open(data_dir / f'{session}.json', 'r', encoding='utf-8') as f:
            group = json.load(f)
    except FileNotFoundError:
        await MARNE_MAIN.send('请先绑定服务器ID.')
        return
    serverID = group['id']
    results = await request_marneapi(serverID)
    result = json.loads(results)
    server_ID = result['id']
    server_name = result['name']
    server_description = result['description']
    server_region = result['region']
    server_country = result['country']
    server_currentPlayers = result['currentPlayers']
    server_maxPlayers = result['maxPlayers']

    with open(data_dir / f'{session}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    player_list = result['playerList']
    sorted_player_list = sorted(player_list, key=lambda x: x['team'])

    team1_counts = 0
    team2_counts = 0
    # 统计每个队伍的人数
    for player in player_list:
        if player['team'] == 1:
            team1_counts += 1
        elif player['team'] == 2:
            team2_counts += 1

    msg = Message([MessageSegment.text(f'查询成功')])
    msg.append(f'\n服务器ID: {server_ID}')
    msg.append(f'\n服务器名字: {server_name}')
    msg.append(f'\n服务器简介: {server_description}')
    msg.append(f'\n服务器区域: {server_region} - {server_country}')
    msg.append(f'\n当前人数: {server_currentPlayers} / {server_maxPlayers}')
    if server_currentPlayers == 0:
        msg.append(f'\n--------------------'
                   f'\n服务器内没有玩家'
                   f'\n--------------------')
        await MARNE_PLST.send(msg,reply_message=True)
        return

    if team1_counts > 0:
        msg.append(f'\n---------- 队伍1 ({team1_counts}) ----------')
        team1_count = 0
        for player in sorted_player_list:
            if player['team'] == 1:
                player_name = player['name']
                team1_count += 1
                msg.append(f'\n{team1_count}. {player_name}')
    else:
        msg.append(f'\n---------- 队伍1无人 ----------')

    if team2_counts > 0:
        msg.append(f'\n---------- 队伍2 ({team2_counts}) ----------')
        team2_count = 0
        for player in sorted_player_list:
            player_name = player['name']
            if player['team'] == 2:
                team2_count += 1
                msg.append(f'\n{team2_count}. {player_name}')
    else:
        msg.append(f'\n---------- 队伍2无人 ----------')

    await MARNE_PLST.finish(msg,reply_message=True)


@MARNE_BIND.handle()
async def _bind(event: GroupMessageEvent, args: Message = CommandArg()):
    session = event.group_id
    serverID = args.extract_plain_text()

    if len(args) == 1 & serverID.isdigit():
        pass
    else:
        await MARNE_PLST.finish('格式错误，仅允许纯数字',reply_message=True)
        return

    result = await request_marneapi(serverID)
    result = json.loads(result)
    serverName = result['name']
    try:
        with open(data_dir / f'{session}.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        data_dir.mkdir(parents=True, exist_ok=True)
        return

    msg = Message([MessageSegment.text(f'绑定成功！')])
    msg.append(f'\n服务器ID: {serverID}')
    msg.append(f'\n服务器名字: {serverName}')

    await MARNE_BIND.send(msg,reply_message=True)
