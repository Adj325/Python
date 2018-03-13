import os
import re
import base64
import datetime
import requests
from http import cookiejar


# 获取验证码
def getimgcheckcode():

    response = session.get(pic_url,  headers=headers)
    pic_base64 = str(response.text).replace('data:image/jpg;base64,','')
    with open('yzm.jpg', 'wb') as pic:
        pic.write( base64.b64decode(pic_base64) )

    login_data['imgcheckcode'] = input('  验证码: ')

# 拆红包主函数
def redpacket_click():
    session.get(redpacket_url, headers=headers)
    headers["Referer"] = 'http://all.17wo.cn'
    r = session.get(redpacket_click_url, headers=headers)
    print('红包提示: {}'.format(r.json()['data']['descri']))

# 首次登录
def first_login(account, pwd):

    login_data['mobile'] = account

    login_data['pwd'] = pwd

    # 获取csrf
    #session = requests.session()
    r = session.get('http://all.17wo.cn/login/login', headers=headers)

    login_data['csrf'] = re.findall('id="csrf" value="(.*?)" /', r.text)[0]

    # 获取验证码
    getimgcheckcode()
    # 提交账号密码及验证码以登录
    r = session.post(login_url, data=login_data, headers=headers)
    while not isLogin(account):
        # 获取验证码
        getimgcheckcode()
        # 获取csrf
        r = session.get(login_url, headers=headers)
        login_data['csrf'] = re.findall('id="csrf" value="(.*?)"', r.text)[0]
        # 再次 提交账号密码及验证码以登录
        session.post(login_url, data=login_data, headers=headers)
    print('登录提示: 登录成功!')

def isLogin(account):
    r = session.get(index_url, headers=headers)

    if account in r.text:
        return True
    else:
        return False

# 签到主函数
def signin_click():
    session.get(signin_click_url, headers=headers)    
    r = session.get(signin_info_url, headers=headers)
    if r.json()['data']['continuousNum'] == 7:
        print('签到提示: 成功签到, 获得50M流量')
    else:
        print('签到提示: 成功签到, 获得5M流量')
        

# 默认主页
index_url = 'http://all.17wo.cn/citic/home'
# 登录主页
login_url = 'http://all.17wo.cn/login/loginPageActionForBusiness'
# 验证码
pic_url = 'http://all.17wo.cn/login/loginpage'

# 签到主页
signin_url = 'http://all.17wo.cn/citic/sign/view'
# 点击签到
signin_click_url = 'http://all.17wo.cn/citic/sign/signin'
# 已签到信息
signin_info_url = 'http://all.17wo.cn/citic/sign/signCount'

# 红包主页
redpacket_url = 'http://all.17wo.cn/redPacket/FlowRedPacket'
# 拆红包
redpacket_click_url = 'http://all.17wo.cn/redPacket/openRedPacket'
# 当前信息
curinfo_url = 'http://all.17wo.cn/citic/home/account'

def curinfo():
    r = session.get(curinfo_url, headers=headers)
    print('当前流量: {}M'.format(r.json()['data']['flow']))
# 表单数据
login_data = {
                'logintype':'passlogin',
                'url':'/login/indexpage',
                'mobile':'',
                'pwd':'',
                'imgcheckcode':'',
                'checkcode':'',
                'source':'',
                'campaign':'',
                'callback':'',
                'csrf':''
             }
# 浏览器模拟
headers = {
    "Host": "all.17wo.cn",
    "Referer": "http://all.17wo.cn/login/loginPageActionForBusiness",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87',
    'Connection': 'keep-alive'
}


today = datetime.datetime.now().strftime("%Y-%m-%d")  # 得到当前的日期和时间  201x-xx-xx格式

# 创建一个session, 方便保存cookies
session = requests.session()

di_acpw = eval(open('acpw.txt', 'r').read())
nft = 1
for account in di_acpw:
    name = di_acpw[account][0]
    pwd = di_acpw[account][1]
    print('\n--------------------------------------------------------')
    print('                正在读取第 {} 个用户!'.format(nft))
    print('--------------------------------------------------------\n')
    print('当前用户: {}\n手机号码: {}'.format(name, account))


    # 判断一起沃目录是否存在
    if not os.path.exists(os.getcwd() + '\\一起沃\\'):
        os.makedirs(os.getcwd() + '\\一起沃\\')
    cookiesName = os.getcwd() + '\\一起沃\\' + account

    session.cookies = cookiejar.LWPCookieJar(filename=cookiesName)
    try:    # 尝试加载cookies
        session.cookies.load(ignore_discard=True)
    except:# 无法加载cookies时,采用账号密码登录
        open(cookiesName, 'w+')
    
    while not isLogin(account):
        first_login(account, pwd)

    try:
        # 签到
        signin_click()
        # 拆红包
        #redpacket_click()
        # 目前信息
        curinfo()
    except:
        first_login(account, pwd)
        # 签到
        signin_click()
        # 拆红包
        #redpacket_click()
        # 目前信息
        curinfo()

    # 保存cookies文件
    session.cookies.save()
    nft += 1
