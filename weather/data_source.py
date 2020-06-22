from  requests import get
async def get_weather_of_city(city: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    try:
        private_key='71683974'
        weather_api = 'https://tianqiapi.com/api?version=v6&appid=71683974&appsecret=R2DVOy0M&city='+city
        dats=get(weather_api).text
        return f'{dats}'
    except :
        return f'无法查询到{city}的数据'
