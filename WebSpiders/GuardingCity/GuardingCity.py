import os
import time
import random
import logging
import datetime
import threading

try:
    import execjs
except:
    os.system('pip install PyExecJS')
    import execjs

try:
    import requests
except:
    os.system('pip install requests')
    import requests
    


with open("sign.js") as f:
    jsData = f.read()
    sign_ctx = execjs.compile(jsData)


def getKey():
    return 'TykA3r6SV8k4EmIzxaKamH9Tg3ZIZUna'


def getTimestamp():
    return str(time.time()).replace('.', '')[:13:]


def getSign(openId, timestamp):
    return sign_ctx.call("b", 'openId={}&timestamp={}&key={}'.format(openId, timestamp, getKey()))


if not os.path.exists('log'):
    os.mkdir('log')

logger = logging.getLogger()
# Log等级开关
logger.setLevel(logging.DEBUG)
# 第二步，创建一个handler，用于写入日志文件
logfile = 'log/' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M') + '_log.log'
print('当前日志文件: ' + logfile)
file_handler = logging.FileHandler(logfile, mode='a+', encoding='utf-8')
# 输出到file的log等级的开关
file_handler.setLevel(logging.INFO)
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
# 第四步，将handler添加到logger里面
logger.addHandler(file_handler)

class Address:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

class User:
    def __init__(self, remark, get_type, openId, name, mobilePhone, addressName, address):
        self.openId = openId
        self.addressName = addressName
        self.mobilePhone = mobilePhone
        self.name = name
        self.remark = remark
        self.get_type = get_type
        self.address = address


get_type_name = {
    'invite': '自取', 'mail': '邮寄'
}

users = []

success_number = 0

# 定位坐标
ZuoBiao = Address(110.7888546, 21.424235)

# 收件地址
address_name = '你家门口'



ua_list = [
    '''Mozilla/5.0 (Linux; Android 9; BKL-AL20 Build/HUAWEIBKL-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045018 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools''',
    '''Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045018 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools''',
    '''Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045018 Mobile Safari/537.36 MicroMessenger/6.3.27.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools''',
    '''Mozilla/5.0 (Linux; Android 8.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045018 Mobile Safari/537.36 MicroMessenger/6.3.19.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools''',
    '''Mozilla/5.0 (Linux; Android 8.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045018 Mobile Safari/537.36 MicroMessenger/6.7.30.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools''',
    '''Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045018 Mobile Safari/537.36 MicroMessenger/7.0.6.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools''',
    '''Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; Mi Note 2 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045018 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools''',
    '''Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5s Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045018 Mobile Safari/537.36 MicroMessenger/6.3.28.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools''',
    '''Mozilla/5.0 (Linux; Android 8.0.0; SM-G9650 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045018 Mobile Safari/537.36 MicroMessenger/7.0.9.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools''',
]

def my_list():
    users_todo = []
    ua = '''Mozilla/5.0 (Linux; Android 9; BKL-AL20 Build/HUAWEIBKL-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045018 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools'''
    now_time = datetime.datetime.now()
    for user in users:
        host = random.choice([
            #'dapi.zjfy.zjzwy.com',
            'dorder.zjfy.zjzwy.com'
            ])
        list_url = 'https://' + host + '/api/book/myBookList.action'
        headers = {
            'Host': host,
            'User-Agent': ua,
            'content-type': "application/x-www-form-urlencoded",
            'charset': 'utf-8',
            'Accept-Encoding': 'gzip',
            #'referer': 'https://servicewechat.com/wxbae5bf540fda1b3e/19/page-frame.html'
        }
        time.sleep(2)
        data = {
            'openId': user.openId
        }
        try:
            r = requests.post(list_url, data=data, headers=headers, timeout=10)
            items = r.json()['data']['pageResult']['items']
            if len(items) != 0:
                item = items[0]
                endPickTime = datetime.datetime.strptime(item['endPickTime'], '%Y-%m-%d %H:%M:%S')
                if item['orderStatus'] == 'wait' and endPickTime > now_time:
                    if item['bookType'] == 'mail':
                        print('○ 待领取: {0} - {1} - {5} - {2:11s} - {3} - {4} - {6}({7})'.format(
                            get_type_name[item['bookType']],
                            item['bookTime'],
                            item['productName'],
                            user.remark,
                            user.mobilePhone,
                            item['ipAddress'], item['name'], item['receiveAddress']))
                    else:
                        print('○ 待领取: {0} - {1} - {6} - {2:11s} - {3} - {4} - {5}'.format(
                            get_type_name[item['bookType']],
                            item['bookTime'],
                            item['productName'],
                            user.remark,
                            item['checkCode'],
                            item['storeAddress'],
                            item['ipAddress']))
                    continue
                else:
                    item_date = endPickTime.date()
                    now_time_date = now_time.date()
                    last = now_time_date - item_date
                    if last.days >= 3:
                        users_todo.append(user)
                        print('√ 可抢购: ' + user.remark + ' - ' + user.name + ' - ' + item['bookTime'])
                    else:
                        if item['orderStatus'] == 'cancel':
                            tip_name = '已取消'
                        else:
                            tip_name = '已领取'
                        if item['bookType'] == 'mail':
                            print('● ' + tip_name + ': {0} - {1} - {5} - {2:11s} - {3} - {4}'.format(
                                get_type_name[item['bookType']],
                                item['bookTime'],
                                item['productName'],
                                user.remark,
                                user.mobilePhone,
                                item['ipAddress']))
                        else:
                            print('● ' + tip_name + ': {0} - {1} - {6} - {2:11s} - {3} - {4} - {5}'.format(
                                get_type_name[item['bookType']],
                                item['bookTime'],
                                item['productName'],
                                user.remark,
                                item['checkCode'],
                                item['storeAddress'],
                                item['ipAddress']))
            else:
                users_todo.append(user)
                print('√ 可抢购: ' + user.remark + ' - ' + user.name + ' - 从未预约')

        except Exception as e:
            print('× 无法获取 {0}-{1:13s} 的预购记录。错误详情: {2}'.format(user.name, user.remark, str(e)))
    print("\n" + str(len(users_todo)) + " 人可抢购\n名单: " + '、'.join([user.remark for user in users_todo]))
    return users_todo


def main(user, timestamp, sign):
    global success_number
    ua = random.choice(ua_list)
    host = random.choice([
        'dapi.zjfy.zjzwy.com',
        #'dorder.zjfy.zjzwy.com'
    ])
    order_url = 'https://' + host + '/api/book/bookOrder.action'

    locationLongitude_2 = user.address.longitude
    locationLatitude_2 = user.address.latitude

    if random.choice([True, False]):
        locationLongitude_2 += random.randrange(10, 20) / 10000000
    else:
        locationLongitude_2 -= random.randrange(10, 20) / 10000000
    if random.choice([True, False]):
        locationLatitude_2 += random.randrange(10, 20) / 10000000
    else:
        locationLatitude_2 -= random.randrange(10, 20) / 10000000
    locationLongitude_2 = str(locationLongitude_2)[:11:]
    locationLatitude_2 = str(locationLatitude_2)[:10:]

    data = {
        'locationLongitude': locationLongitude_2,
        'locationLatitude': locationLatitude_2,
        'name': user.name,
        'addressName': user.addressName,
        'mobilePhone': user.mobilePhone,
        'type': user.get_type,
        'openId': user.openId,
        'sign': sign,
        'timestamp': timestamp
    }

    headers = {
        'Host': host,
        'User-Agent': ua,
        'content-type': "application/x-www-form-urlencoded",
        'charset': 'utf-8',
        'Accept-Encoding': 'gzip',
        #'referer': 'https://servicewechat.com/wxbae5bf540fda1b3e/0/page-frame.html'
    }

    try:
        r = requests.post(order_url, data=data, headers=headers, timeout=10)
        if 'true' in r.text:
            success_number = success_number + 1
            checkCode = r.json()['data']['order']['checkCode']
            print('\n抢购结果: 成功, ' + user.remark + ' ' + r.text)
            logger.info('\n抢购结果: 成功, ' + user.remark + ' ' + r.text)
            logger.info('{}-{}-{}-{}-{}'.format(user.name, user.mobilePhone, user.remark, user.openId, checkCode))
        else:
            print('\n抢购结果: ' + user.remark + ' 抢购失败，原因: ' + r.json()['data']['errorMsg'])
    except Exception as e:
        print('请求错误，' + user.remark + ' ' + str(e))


# 抢购方式: common_mail-邮寄, invite-自取

## 待抢购
# 邮寄-地点一
# users.append(User('邮寄-001', 'common_mail', '微信openid', '联系人名称', '手机号码', '收件地址', ZuoBiao))
# 自取-地点二
# users.append(User('自取-002', 'invite', '微信openid', '联系人名称', '手机号码', '收件地址', ZuoBiao))


success_number = 0

# 定时抢购参数
start_buy_time = '2020-02-23 15:00:02'
end_buy_time = '2020-02-23 15:02:02'
refresh_seconds = 60
# 马上抢购，持续秒数
max_last_seconds = 60 * 10

print('当前时间: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

while True:
    choice = input('\n1-查看预约记录，2-定时抢口罩，其它-马上抢口罩\n输入: ')
    print()
    if choice == '1':
        my_list()
    elif choice == '2':
        start_buy_time_ = datetime.datetime.strptime(start_buy_time, '%Y-%m-%d %H:%M:%S')
        end_buy_time_ = datetime.datetime.strptime(end_buy_time, '%Y-%m-%d %H:%M:%S')

        last_time = datetime.datetime.now()
        print('抢购时间: ' + start_buy_time)
        print('当前时间: ' + last_time.strftime("%Y-%m-%d %H:%M:%S"))

        while True:
            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")

            if (now_time - last_time).total_seconds() > refresh_seconds:
                print('当前时间: ' + now_time_str)
                last_time = now_time

            if success_number == len(users):
                print('\n停止抢购。原因: 所有用户均抢购成功。')
                break

            if (now_time - end_buy_time_).total_seconds() >= 0:
                print('\n停止抢购。原因: 到达停止时间 ' + end_buy_time + ' 。')
                break
            if (now_time - start_buy_time_).total_seconds() >= 0:
                for user in users:
                    timestamp = getTimestamp()
                    sign = getSign(user.openId, timestamp)
                    threading.Thread(target=main, args=(user, timestamp, sign)).start()
                    time.sleep(random.randint(1, 2))
    else:
        start_time = datetime.datetime.now()
        while True:
            if success_number == len(users):
                print('\n停止抢购。原因: 所有用户均抢购成功。')
                break

            now_time = datetime.datetime.now()
            last_time = now_time - start_time

            if last_time.total_seconds() > max_last_seconds:
                print('\n5停止抢购。原因: 已连续抢购 ' + str(max_last_seconds) + ' 秒。')
                break

            for user in users:
                print('替 ' + user.remark + ' 发起抢购。')
                timestamp = getTimestamp()
                sign = getSign(user.openId, timestamp)
                threading.Thread(target=main, args=(user, timestamp, sign)).start()
                time.sleep(random.randint(1, 2))
