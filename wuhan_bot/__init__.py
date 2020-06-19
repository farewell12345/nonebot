import nonebot
from nonebot import on_natural_language, NLPSession, IntentCommand, NLPResult
from nonebot import on_command,CommandSession
from .get_data import *
@on_command('wuhan',aliases=('test'))
async def wuhan(session:CommandSession):
    src=await get_virus(await now_index())
    await session.send(str(src))
    news=await get_news(await now_news())
    await session.send(str(news))
@on_natural_language(keywords=('疫情'),only_to_me=False)
# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
async def _(session:NLPResult):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    # 置信度的计算需要自然语言处理器的编写者进行恰当的设计，以确保各插件之间的功能不会互相冲突。
    # 在 NoneBot 中，自然语言处理器的工作方式就是将用户的自然语言消息解析成一个命令和命令所需的参数，
    # 由于自然语言消息的模糊性，在解析时不可能完全确定用户的意图，因此还需要返回一个置信度作为这个命令的确定程度。
    #
    return IntentCommand(90.0,'wuhan')





