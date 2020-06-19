from nonebot import *
import nonebot
import json
import requests
import datetime
import re
import lxml
from bs4 import BeautifulSoup
def dict_to_json(data):
    data=str(data).replace(']','').replace('[','').replace('\'','\"')
    return data
@on_command("ACG",only_to_me=False,aliases=("\新番","\新番时间表"))
async def ACG(session:CommandSession):
    a = ''
    try:
        a = session.event['group_id']
    except:
        pass
    if a == 586078667:
        return
    data=requests.get("https://bangumi.bilibili.com/web_api/timeline_global").json()
    if data['message']=='success':
        ACG=data['result']
        # ACG= test["seasons"]
        data=str(datetime.datetime.today().month)
        day=str(datetime.datetime.today().day)
        for j in ACG:
            if j["date"]==data+"-"+day:
                ACG=j["seasons"]
                break
        for i in ACG:
            title=i['title']
            if re.search("僅限台灣地區",title) or re.search("僅限港澳台地區",title):
                continue
            index=i['pub_index']
            time=i['pub_time']
            src+=f'{title}({index})  :  {time}\n--------\n'
        src=list(src)
        src[len(src)-1]=''
        src=''.join(src)
        await session.send(src)