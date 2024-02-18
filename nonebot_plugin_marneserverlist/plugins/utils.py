import requests
import json
from nonebot import get_plugin_config
from .config import Config

plugin_config = get_plugin_config(Config)
marne_url = plugin_config.marne_url
    
def request_marneAPI(serverID):
    print(f"{marne_url}api/srvlst/{serverID}")
    response = requests.get(f"{marne_url}api/srvlst/{serverID}")
    response.raise_for_status()  # 如果请求失败，则引发适当的异常
    if response.status_code == 200:
        return response.text
    else:
        raise requests.HTTPError