from nonebot import on_command,CommandSession,NLPSession
import json
from jieba import posseg
from nonebot import on_natural_language,NLPResult,IntentCommand
from .get_translate import *


@on_command('translate',aliases=('\翻译'))
async def weather(session:CommandSession):
    word=session.get('word',prompt='你想翻译什么？')#尝试从当前对话中获取city参数，如果找不到就会抛出异常
    src=''
    try:
        words=''.join(str(word).split()).encode('UTF-8')
        if words.isalpha():
           src= get_translate_English(word)
        else:
           src= get_translate_Chinese(word)
    except :
        src="暂时没有这个词的翻译！"
    await session.send(src)

@on_natural_language(keywords=('\翻译'),only_to_me=False)
# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
async def _(session:NLPSession):
    stripped_msg=session.msg_text
    word_=str(stripped_msg).replace("\翻译",'')
    # words=posseg.lcut(stripped_msg)
    # word_=None
    # for word in words:
    #     if word.flag=='ns':
    #         # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
    #         word_=word.word
    #         break
    return IntentCommand(90.0,'translate',current_arg=word_ or '')

@weather.args_parser
async def _(session:CommandSession):#weather的命令解析器
    stripped_arg=session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['word']=stripped_arg
        return
    if not stripped_arg:
        session.pause("单词名称不能为空哦")
    session.state[session.current_key]  =stripped_arg