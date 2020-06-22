import re

from nonebot import on_natural_language, NLPSession, on_command, CommandSession
from requests import *
from .userClass import *


@on_natural_language(only_to_me=False, keywords=('添加游戏：'))
async def addGames(session: NLPSession):
    try:
        msg = session.msg_text
        send_user = session.event['user_id']
        if re.search('添加游戏：(.+?)', msg) is not None and re.search('[CQ:]', msg) is None:
            msg = str(msg).replace(''.join(re.findall('(.+?)添加游戏：', msg)), '').replace(' ', '').replace('添加游戏：', '')
            if msg != '':
                for i in gameList:
                    if i.gameName == msg:
                        await session.send('已经存在该游戏，请回复加入游戏后加入该游戏')
                        return
                else:
                    addGame(gameGroup(FirstId=send_user, gameName=msg).getThis())
                    await session.send(f"添加游戏{msg}成功！")
    except:
        pass


@on_natural_language(only_to_me=False, keywords=('查询人数：'))
async def searchGamers(session: NLPSession):
    try:
        msg = session.msg_text
        if re.search('查询人数：(.+?)', msg) is not None and re.search('[CQ:]', msg) is None:
            msg = str(msg).replace('查询人数：', '').replace(' ', '')
            if msg != '':
                for i in gameList:
                    if i.gameName == msg:
                        await session.send(f'{i.gameName}:当前人数{i.getGmaersNum()}')
                        return
                else:
                    await session.send(f"暂无游戏{msg}")
    except:
        pass


@on_natural_language(only_to_me=False, keywords=('删除游戏：'))
async def deletGames(session: NLPSession):
    try:
        msg = session.msg_text
        if re.search('删除游戏：', msg) is not None and re.search('[CQ:]', msg) is None:
            msg = str(msg).replace('删除游戏：', '').replace(' ', '')
            if msg != '':
                for i in gameList:
                    if i.gameName == msg:
                        deleteGmae(i)
                        await session.send(f"删除游戏{msg}成功！")
                        return
                else:
                    await session.send(f"没有游戏{msg}！")
    except:
        pass


@on_natural_language(only_to_me=False, keywords=('退出游戏：'))
async def deletGames(session: NLPSession):
    try:
        msg = session.msg_text
        send_user = session.event['user_id']
        if re.search('退出游戏：', msg) is not None and re.search('[CQ:]', msg) is None:
            msg = str(msg).replace('退出游戏：', '').replace(' ', '')
            if msg != '':
                for i in gameList:
                    if i.gameName == msg:
                        i.removeGamer(id=send_user)
                        await session.send(f"退出游戏：{msg}成功！")
                        if i.getGmaersNum()==0:
                            deleteGmae(i)
                            await session.send(f"游戏：{msg}无人参加，已自动删除！")
                        return
                else:
                    await session.send(f"没有游戏{msg}！")
    except:
        pass


@on_natural_language(only_to_me=False, keywords=('加入游戏：'))
async def addGames(session: NLPSession):
    try:
        msg = session.msg_text
        send_user = session.event['user_id']
        if re.search('加入游戏：', msg) is not None:
            msg = str(msg).replace('加入游戏：', '').replace(' ', '')
            if msg != '':
                for i in gameList:
                    if i.gameName == msg:
                        await session.send(i.addFriend(id=send_user))
                        return
                else:
                    await session.send("暂无此游戏,请回复创建游戏：+游戏名创建新游戏组")
    except:
        pass


@on_natural_language(only_to_me=False, keywords=('来：'))
async def starGamers(session: NLPSession):
    try:
        msg = session.msg_text
        if re.search('来：', msg) is not None:
            msg = str(msg).replace('来：', '').replace(' ', '')
            if msg != '':
                for i in gameList:
                    if i.gameName == msg:
                        await session.send(i.printGamer())
                        return
                else:
                    await session.send("暂无此游戏,请回复创建游戏：+游戏名创建新游戏组")
    except:
        pass


@on_command('getAllGames', aliases=('查询游戏列表'), only_to_me=False)
async def getAllGames(session: CommandSession):
    if len(gameList) >= 0:
        src = ''
        for i in gameList:
            src += i.gameName + f'：已有人数:{i.getGmaersNum()}\n'
        await session.send(src)
    else:
        await session.send('暂无游戏')
