from nonebot import on_command, CommandSession
import json
from jieba import posseg
from nonebot import on_natural_language,NLPResult,IntentCommand
from .data_source import get_weather_of_city



@on_command('weather',aliases=('\天气','\天气预报','\天气查询','\查询天气'))
async def weather(session:CommandSession):
    city=session.get('city',prompt='你想查询哪个城市的天气？')#尝试从当前对话中获取city参数，如果找不到就会抛出异常
    weather_report=await get_weather_of_city(city)
    if weather_report!='无法查询到{city}的数据':
        weather_report = json.loads(weather_report)
        weather_index=city+'的天气为：'+weather_report['wea']+'\n'\
                      +'当前温度'+weather_report['tem']+'℃'+'\n'\
                      +'本日温度：'+weather_report['tem1']+'℃'+'~'+weather_report['tem2']+'℃'+'\n'\
                      +'今日风向：'+weather_report['win']+weather_report['win_speed']+'\n'\
                      +'今日'+city+'空气质量：'+weather_report['air_level']+'\n'\
                      +weather_report['air_tips']
        await session.send(weather_index)
    else:
        await session.send(weather_report)
@on_natural_language(keywords=('/天气','/预报'),only_to_me=False)
# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
async def _(session:NLPResult):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    # 置信度的计算需要自然语言处理器的编写者进行恰当的设计，以确保各插件之间的功能不会互相冲突。
    # 在 NoneBot 中，自然语言处理器的工作方式就是将用户的自然语言消息解析成一个命令和命令所需的参数，
    # 由于自然语言消息的模糊性，在解析时不可能完全确定用户的意图，因此还需要返回一个置信度作为这个命令的确定程度。
    #
    stripped_msg=session.msg_text.strip()
    words=posseg.lcut(stripped_msg)
    city=None
    for word in words:
        if word.flag=='ns':
            # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
            city=word.word
            break
    return IntentCommand(90.0,'weather',current_arg=city or '')

@weather.args_parser
async def _(session:CommandSession):#weather的命令解析器
    stripped_arg=session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['city']=stripped_arg
        return
    if not stripped_arg:
        session.pause("城市名称不能为空哦")
    session.state[session.current_key]  =stripped_arg