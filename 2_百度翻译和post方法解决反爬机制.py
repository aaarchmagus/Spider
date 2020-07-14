# 1.导入request库
import requests
import json
from pprint import pprint

# 2.发起请求获取响应,注意移动端的url也发生了变化
url = "https://fanyi.baidu.com/basetrans"

query = input("请输入您需要翻译的词汇：")

"""通过移动端进行爬取解决反爬"""
data = {
    "from": "en",
    "to": "zh",
    "query": query,

}

headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36",
    "Cookie":"BAIDUID=21486F6479B4EFBFB1327E634F5D49D7:FG=1; BIDUPSID=21486F6479B4EFBFB1327E634F5D49D7; PSTM=1463475659; PSINO=2; H_PS_PSSID=1433_21116_22075; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; locale=zh; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1537926127; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1537926127; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1537923769,1537926127; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1537926127",
    "Referer":"https://fanyi.baidu.com/"
}


response = requests.post(url,headers=headers,data=data)
pprint(json.loads(response.text)['trans'][0]['dst'])

