# 1.导入request库
import requests

# 2.发起请求获取响应
url = "https://tieba.baidu.com/f"

headers = {
"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}


kw = input("请输入贴吧的名称： ")

for pn in range(0,150,50):
    params = {
        "kw":kw,
        "pn":pn
    }

    response = requests.get(url,params=params,headers=headers)
    # response.content 响应二进制数据
    # 3.解析响应数据
    with open("2_tieba_{}.html".format(pn),"wb")as f:
        f.write(response.content)
