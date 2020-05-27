'''
调用百度的接口识别图片内容
https://ai.baidu.com console
'''
import json

from aip import AipOcr

# my APPID AK SK
APP_ID = "18623047"
API_KEY = "RZp5GIyGN3UbD4TMUg8gYA6L"
SECRET_KEY = "UkQ4ndMeNWX358AHNn9oDMnSo82mCaex"
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def recognize_pic(file):
    image = get_file_content(file)
    client.basicGeneral(image)
    # 可选参数
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"
    options["recognize_granularity"] = "big"
    # 带参数调用通用文字识别, 图片参数为本地图片 """
    info = client.basicAccurate(image, options)
    # print(info)
    dict_words={}
    listwords=[]
    words_info = info['words_result']
    for i in range(len(words_info)):
        word = words_info[i]['words']
        listwords+=list(word)
    dict_words['content']=listwords
    return json.dumps(dict_words,ensure_ascii=False)
        #print(word)

result=recognize_pic('4_struct.png')
print(''.join(eval(result)['content']))
# print(''.join(result['content']))
