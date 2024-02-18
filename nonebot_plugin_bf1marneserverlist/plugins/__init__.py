from nonebot import on_command
from nonebot import get_plugin_config
from nonebot.adapters.onebot.v11 import GROUP, Message, MessageEvent, MessageSegment, GroupMessageEvent
from nonebot.typing import T_State
from nonebot.params import CommandArg, Depends, _command_arg
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER

import httpx
from .config import Config

from pathlib import Path
import json
import httpx

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-bf1marneserverlist",
    description="Onebot plugin for Battlefield 1 Marne",
    usage="type /marne bind {serverID} and send /marne",

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="https://github.com/SAFEluren/nonebot-plugin-bf1marneserverlist",
    # 发布必填。

    config=Config,
    # 插件配置项类，如无需配置可不填写。

    supported_adapters={"~onebot.v11"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

plugin_config = get_plugin_config(Config)

marne_url = plugin_config.marne_url
    
CURRENT_FOLDER = Path(plugin_config.marne_data_dir).resolve()
CURRENT_FOLDER.mkdir(parents=True,exist_ok=True)

async def is_enable() -> bool:
    return plugin_config.marne_plugin_enabled

MARNE_MAIN = on_command(f'marne', block=True, priority=1)
MARNE_BIND = on_command(f'marne bind', block=True, priority=1,permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER)
MARNE_MODS = on_command(f'marne modlist', block=True, priority=1)

async def request_marneAPI(serverID):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{marne_url}api/srvlst/{serverID}")

            content = response.text
            if content is not None:
                return content
            else:
                print("Response content is None")

    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")

@MARNE_MAIN.handle()
async def marne_info(event:GroupMessageEvent, state:T_State):
    session = event.group_id

    try:
        with open(CURRENT_FOLDER/f'{session}.json','r', encoding='utf-8') as f:
            group = json.load(f)
    except FileNotFoundError:
        await MARNE_MAIN.send('请先绑定服务器ID.')
        return
    serverID = group['id']
    results = await request_marneAPI(serverID)
    if results is not None:
        result = json.loads(results)
    else:
        print("Response content is None")

    if result:
        server_ID = result['id']
        server_name = result['name']
        server_description = result['description']
        server_region = result['region']
        server_country = result['country']
        server_map = result['map']
        server_mode = result['mode']
        server_currentPlayers = result['currentPlayers']
        server_maxPlayers = result['maxPlayers']
        
        with open(CURRENT_FOLDER/f'{session}.json','w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        msg = Message([MessageSegment.text(f"查询成功")])
        msg.append(f"\n绑定的服务器ID :{server_ID}")
        msg.append(f"\n服务器名字:{server_name}")
        msg.append(f"\n服务器简介:{server_description}")
        msg.append(f"\n服务器区域:{server_region} - {server_country}")
        msg.append(f"\n当前地图:{server_map}")
        msg.append(f"\n游戏模式:{server_mode}")
        msg.append(f"\n当前人数:{server_currentPlayers} / {server_maxPlayers}")
        
        await MARNE_BIND.send(msg)
        # await MARNE_BIND.send(f'已绑定服务器ID:{serverID}')
    else:
        print(result)
        await MARNE_MAIN.send('无法获取到服务器数据，请检查马恩服务器id是否正确，或服务器当前未开启。')
        return

@MARNE_MODS.handle()
async def marne_mods(event:GroupMessageEvent, state:T_State):
    message = _command_arg(state) or event.get_message()
    session = event.group_id

@MARNE_BIND.handle()
async def marne_bind(event: GroupMessageEvent, state: T_State):
    message = _command_arg(state) or event.get_message()
    session = event.group_id
    args = message.extract_plain_text().strip().split(' ')
    print(args[0])
    try:
        serverID = int(args[0])
    except ValueError:
        await MARNE_BIND.send('格式错误，仅允许纯数字')
        return  # 在这里返回，避免继续执行代码

    print(serverID)
    result = await request_marneAPI(serverID)  # 等待异步函数完成
    results = await request_marneAPI(serverID)
    if results is not None:
        result = json.loads(results)
        serverName = result['name']
        try:
            with open(CURRENT_FOLDER / f'{session}.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            CURRENT_FOLDER.mkdir(parents=True,exist_ok=True)
            return

        msg = Message([MessageSegment.text(f"绑定成功！")])
        msg.append(f"\n绑定服务器ID :{serverID}")
        msg.append(f"\n服务器名字:{serverName}")

        await MARNE_BIND.send(msg)
        # await MARNE_BIND.send(f'已绑定服务器ID:{serverID}')
    else:
        print(result)
        await MARNE_MAIN.send('无法获取到服务器数据，请检查马恩服务器id是否正确，或服务器当前未开启。')