import json
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
import nonebot
import pytz
from nonebot import on_command, scheduler
from aiocqhttp.exceptions import Error as CQHttpError
from .lesson import *
from awesome.plugins.date_time_study.config import *
from .lessons_index import *


async def send_command(class_name):
    bot = nonebot.get_bot()
    for i in GROUP_ID:
        group_user_list = await bot.get_group_member_list(group_id=i, self_id=2624672407)
        src = ''
        for m in group_user_list:
            a = m['user_id']
            src = src + '[CQ:at,qq=' + str(a) + ']'
        await bot.send_group_msg(group_id=i, message=src)
        for j in range(0, len(group_user_list)):
            try:
                a = group_user_list[j]['user_id']
                await bot.send_private_msg(user_id=a, message="test")
                j += 1
            except:
                print("无好友关系")
                j += 1


async def send_friend(classes, i, class_name, teach_ul):
    bot = nonebot.get_bot()
    src = ''
    for m in classes:
        src = src + '[CQ:at,qq=' + str(m) + ']'
    await bot.send_group_msg(group_id=i, message=src)
    for j in range(0, len(classes)):
        try:
            a = classes[j]
            await bot.send_private_msg(user_id=a, message=f'请前往{teach_ul}上{class_name}')
        except:
            print("无好友关系")
        finally:
            j += 1


async def our_send(classes, class_name, teach_ul):
    bot = nonebot.get_bot()
    for i in GROUP_ID:
        if i == 569209282:
            await bot.send_group_msg(group_id=i, message=classes + f'班注意')
            three = (1149558764, 1015656665, 1043824756)
            six = (1980187057, 2321520339, 1596061110)
            if classes == '3':
                await send_friend(three, i, class_name, teach_ul)
            else:
                await send_friend(six, i, class_name, teach_ul)
            try:
                await send_class(class_name, teach_ul,i)
            except:
                await bot.send_private_msg(user_id=1149558764, message="在发送班级时出错！")
        elif i==586078667 and classes=='3':
            try:
                await send_class(class_name, teach_ul,i)
            except:
                await bot.send_private_msg(user_id=1149558764, message="在发送班级时出错！")

async def mon(week):
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
        4: fri_switch_six,
    }
    today = datetime.today()
    time = today.hour
    print('执行今日课程')
    try:
        clas_name = lesson_dict_three[week][time]
        try:
            b = three_teach[clas_name]
            try:
                await our_send('3', clas_name, b)
            except:
                print("发送失败！")
                await nonebot.get_bot().send_private_msg(user_id=1149558764, message='三班发送课程出错！')
        except:
            print("获取教学地点失败！")
            await nonebot.get_bot().send_private_msg(user_id=1149558764, message='获取教学地点失败！')
    except:
        print("三班无课")

    try:
        clas_name = lesson_dict_six[week][time]
        try:
            b = three_teach[clas_name]
            try:
                await our_send('6', clas_name, b)
            except:
                print("发送失败！")
                await nonebot.get_bot().send_private_msg(user_id=1149558764, message='六班发送课程出错！')
        except:
            print("获取教学地点失败！")
            await nonebot.get_bot().send_private_msg(user_id=1149558764, message='获取教学地点失败！')
    except:
        print("六班无课")
        return
