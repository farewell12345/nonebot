from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
import nonebot
import pytz
from requests import *
from nonebot import on_command, scheduler
from aiocqhttp.exceptions import Error as CQHttpError
from nonebot import on_natural_language, NLPSession, IntentCommand, NLPResult, session, on_request
from nonebot import on_command, CommandSession
from awesome.plugins.date_time_study.config import GROUP_ID
from .mon import *
from .config import *


@on_command('Query', aliases=('查询下节课', '下节课查询'), only_to_me=False)
async def Query(session: CommandSession):
    lesson_dict_three = {
        0: mon_switch_three,
        1: tue_switch_three,
        2: web_switch_three,
        3: thu_switch_three,
        4: fri_switch_three}
    lesson_dict_six = {
        0: mon_switch_six,
        1: tue_switch_six,
        2: web_switch_six,
        3: thu_switch_six,
        4: fri_switch_six
    }
    d = datetime.today().weekday()
    time = datetime.today().hour
    try:
        day_class = lesson_dict_three[d]
        while (True):
            try:
                next_class = day_class[time]
                await session.send(f"三班下节课是{time}:50{next_class}")
                break
            except:
                time += 1
            finally:
                if time >= 18:
                    d = d + 1
                    try:
                        day_class = lesson_dict_three[d][7]
                    except:
                        day_class = lesson_dict_three[d][9]
                    await session.send(f"三班下节课是明天的{day_class}")
                    d = d - 1
                    break
    except:
        await session.send(f"明日为周六日，三班无课")
    try:
        a = ''
        try:
            a = session.event['group_id']
        except:
            pass
        if a == 586078667:
            return
        six_day_class = lesson_dict_six[d]
        while (True):
            try:
                next_class = six_day_class[time]
                await session.send(f"六班下节课是{next_class}")
                break
            except:
                time += 1
            finally:
                if time > 18:
                    d += 1
                    time = 7
                    while (True):
                        try:
                            next_class = six_day_class[time]
                            await session.send(f"六班下节课是{time}:50{next_class}")
                            break
                        except:
                            time += 1
                    break
    except:
        await session.send("今日六班无课")


@on_command('getNews', aliases=('新闻'), only_to_me=False)
async def news(session: CommandSession):
    src = get_news()
    await  session.send(src)


def get_news():
    src = '午间新闻：\n'
    url = 'https://v1.alapi.cn/api/new/toutiao'
    data = get(url).json()['data']
    for i in data:
        src += '\n' + i['title'] + '\n'  + i['m_url'] + '\n' + i['time'] + '\n--------------------'
    return src


@nonebot.scheduler.scheduled_job(
    'cron',
    day='*',
    hour='12'
)
async def afternoon_news():
    src = get_news()
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=586078667, message=src)


@nonebot.scheduler.scheduled_job(
    'cron',
    day_of_week='0-5',
    hour='6-18',
    minute='50'
)
async def _():
    d = datetime.today().weekday()
    try:
        print(d)
        try:
            await mon(d)
        except:
            return
    except:
        return
