from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
import nonebot
import pytz
from nonebot import on_command, scheduler
from aiocqhttp.exceptions import Error as CQHttpError

from awesome.plugins.date_time_study.config import GROUP_ID


async def send_class(class_name, teach_ul,i):
    bot = nonebot.get_bot()
    now = str(datetime.today().hour) + ':' + str(datetime.today().minute)
    try:
        await bot.send_group_msg(group_id=i, message=f'现在已经{now}啦，请前往{teach_ul}准备上{class_name}要并记得签到！')
    except CQHttpError:
        pass
