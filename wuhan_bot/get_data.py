import json
from requests import get
async def now_index():
    url='http://www.dzyong.top:3005/yiqing/total'
    datas=get(url).json().get('data')
    return f'{datas}'
async def now_news():
    url='http://www.dzyong.top:3005/yiqing/news'
    datas=get(url).json().get('data')[0]
    return f'{datas}'
async def get_news(news):
    news =news.replace("\'", '\"')
    new = json.loads(news)
    title = new['title']
    source_url = new['sourceUrl']
    src = title + '\n' + source_url
    return src
async def get_virus(data):
    data=data.replace("\'", '\"').replace('[','').replace(']','')
    data=eval(data)
    diagnosed=data['diagnosed']
    death=data['death']
    cured=data['cured']
    date=data['date']
    src='截至'+str(date)+'\n'+'国内目前累计确诊:'+str(diagnosed)+'\n'+'累计死亡:'+str(death)+'\n'+'累计治愈：'+str(cured)+'\n'+'现存确诊(含疑似）'+str(diagnosed-cured-death)
    return src
async def search(city):
    url='http://'