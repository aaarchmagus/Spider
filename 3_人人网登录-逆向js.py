# 1.导入库
import requests
import json
import js2py

# 2. 准备数据发起请求
headers = {
"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}

response = requests.get(url="http://activity.renren.com/livecell/rKey", headers=headers)

n = json.loads(response.text)["data"]

context = js2py.EvalJs()
context.t = {
    "phoneNum": "13621860248",
    "password": "A9900a2a!",
    "c1": "-100"
}

with open('BigInt.js', 'r', encoding='utf-8')as f:
    context.execute(f.read())

with open('RSA.js', 'r', encoding='utf-8')as f:
    context.execute(f.read())

with open('Barrett.js', 'r', encoding='utf-8')as f:
    context.execute(f.read())

context.n = n

js = '''
t.password = t.password.split("").reverse().join("");
setMaxDigits(130);

var o = new RSAKeyPair(n.e,"",n.n);

r = encryptedString(o, t.password);
t.password = r,
t.rKey = n.rkey
'''

context.execute(js)

print(context.t)

data = {
    "c1": "-100",
    "password": context.t.password,
    "phoneNum": context.t.phoneNum,
    "rKey": context.t.rKey
}
session = requests.session()

# 网络请求发启动
session.post("http://activity.renren.com/livecell/ajax/clog", headers=headers, data=data)

response = session.get("http://www.renren.com")

with open("15-reren.html", 'wb') as f:
    f.write(response.content)
