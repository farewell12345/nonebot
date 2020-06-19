from nonebot import on_natural_language, NLPSession, on_command, CommandSession
from requests import *

tempLove = ''


async def get_rainbow_fuck():
    try:
        url = "https://chp.shadiao.app/api.php"
        data = get(url).text
    except :
        data="次数达到上限"
    return data


@on_command('talk_littleMoon', aliases=('召唤小月'), only_to_me=False)
async def sex_pic(session: CommandSession):
    try:
        await session.send(message='[CQ:at,qq=' + str(2689514022) + ']')
    except:
        pass


@on_natural_language(keywords=('夸我'), only_to_me=False)
async def youAreGood(session: NLPSession):
    global tempLove
    if tempLove == '':
        tempLove =await get_rainbow_fuck()
        await session.send(message=tempLove, at_sender=True)
    else:
        await session.send(message=tempLove, at_sender=True)
    tempLove =await get_rainbow_fuck()
