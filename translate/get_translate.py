import hashlib
import time
import uuid
import requests

url = 'https://openapi.youdao.com/api'
APP_ID = '45a132825a61cef4'
APP_KEY = 'coTBoQjo3vi6tHwpDs1JDlMpslml98z2'


def get(form, to, word):
    data = {}
    data['from'] = form
    data['to'] = to
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    data['curtime'] = curtime
    src = APP_ID + truncate(word) + salt + curtime + APP_KEY
    sign = encrypt(src)
    data['appKey'] = APP_ID
    data['q'] = word
    data['salt'] = salt
    data['sign'] = sign
    response = do_request(data).json()
    return response


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    q_utf8 = q.decode("utf-8")
    size = len(q_utf8)
    return q_utf8 if size <= 20 else q_utf8[0:10] + str(size) + q_utf8[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(url, data=data, headers=headers)


def get_translate_Chinese(word):
    word=word.encode('UTF-8')
    response = get('zh-CHS', 'en', word)
    try:
        translate=''
        translates = response.get('translation')
        for i in translates:
            translate = translate+i
        try:
            web=response.get('web')
            for i in web.get('value'):
                translate=translate+';'+i
        except :
            pass
        try:
            explains = response.get('basic')
            for i in explains.get('explains'):
                translate = translate+';' + i
        except:
            pass
        src = '翻译：\n' + translate
        return src
    except:
        return '暂无此词翻译'


def get_translate_English(word):
    word=word.encode('UTF-8')
    response = get('en', 'zh-CHS', word)
    try:
        translate=''
        try:
            translates = response.get('translation')
            for i in translates:
                translate = translate+i+'\n'
        except:
            pass
        try:
            explains = response.get('basic')
            for i in explains.get('explains'):
                translate = translate+i+'\n'
        except:
            pass
        src = '翻译：\n' + translate
        return src
    except :
        return '暂无此词翻译'
