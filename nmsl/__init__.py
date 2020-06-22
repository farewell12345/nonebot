from nonebot import *
import nonebot
import json
import requests
import datetime
import re
import lxml
import re
from bs4 import BeautifulSoup

task = []


@on_natural_language(keywords=('骂他'), only_to_me=False)
async def _(session: NLPSession):
    a = ''
    try:
        a = session.event['group_id']
    except:
        pass
    if a == 586078667:
        return
    bot = nonebot.get_bot()
    at = session.event['raw_message'].replace('骂他', '')
    if re.search('CQ:at,qq=', at) is not None:
        at = re.findall(r"\[CQ:at,qq=([\s\S]+?)\]", at)[0]
    else:
        await session.send("说清楚喽，骂谁", at_sender=True)
        return
    bot_id = str(session.event['self_id'])
    if re.search(bot_id, at) is not None:
        at = '[CQ:at,qq=' + str(session.event['sender']['user_id']) + ']'
    else:
        at = '[CQ:at,qq=' + at + ']'
    url = 'https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn'
    if len(task) == 0:
        src = requests.get(url).text
        task.append(src)
    await session.send(task[0] + at)
    task.clear()
    src = requests.get(url).text
    task.append(src)


@on_natural_language(keywords=('nmsl', '操你妈', '逼逼', '骂我'), only_to_me=False)
async def nmsl(session: NLPSession):
    a = ''
    try:
        a = session.event['group_id']
    except:
        pass
    if a == 586078667:
        return
    who = session.event['sender']['user_id']
    url = 'https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn'
    if len(task) == 0:
        src = requests.get(url).text
        task.append(src)
    await session.send(task[0], at_sender=True)
    task.clear()
    src = requests.get(url).text
    task.append(src)
