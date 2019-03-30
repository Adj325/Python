import re
import os
import execjs
import requests
from urllib import parse

js_sigu = '''
function getSigu(message){
	var key_base = 'contentWindowHig';
	var iv_base = 'contentDocuments';
	var key_base_md5 = CryptoJS.MD5(key_base);
	var key_base_md5_utf8 = CryptoJS.enc.Utf8.parse(key_base_md5);
	var iv_base_utf8 = CryptoJS.enc.Utf8.parse(iv_base);
	var message_encrypted = CryptoJS.AES.encrypt(message, key_base_md5_utf8, {
		'iv': iv_base_utf8,
		'mode': CryptoJS.mode.CBC,
		'padding': CryptoJS.pad.ZeroPadding
	});
	return message_encrypted.toString();
}

'''

with open("sign.js") as f:
    jsData = f.read()
    sign_ctx = execjs.compile(jsData)

with open("crypto-js.js") as f:
    jsData = f.read()
    sigu_ctx = execjs.compile(jsData+js_sigu)

def getSign(text):
    return sign_ctx.call("sign", text)

def getSigu(text):
    return sigu_ctx.call("getSigu", text)

def getHmd5Str(html):
    string = re.findall('eval\("(.*?)"\);', html)[0]
    string = string.split('\\')[1:]
    s = ''
    for i in string[17:49]:
        s += chr(int('0'+i, 16))
    return s

def getSiguStr(html):
    return re.findall('"key":sigu\("(\d+)"\)', html)[0]

def download_m3u8(url, name):
    print('\nm3u8:', url)
    domain = re.findall("https?://.*?/", url)[0]
    print('domain:', domain)
    download_path = os.getcwd() + os.sep +"download"
    file_name = download_path + os.sep + name + '.ts'
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    all_content = requests.get(url).text # 获取M3U8的文件内容

    
    file_line = all_content.split("\n") # 读取文件里的每一行
    for index, line in enumerate(file_line):
        if '.m3u8' in line:
            print('forward:', domain+line[1::])
            download_m3u8(domain+line[1::], name)
            return
        elif ".ts" in line:
            if 'http' not in line:
                line = domain + line[1::]
            print(line)
            res = requests.get(line)
            with open(file_name, 'ab') as f:
                f.write(res.content)
                f.flush()
    else:
        print("提示: {} 下载完成".format(name))

def download_mp4(url_list, name):
    print('\nurl_list_size:', len(url_list))
    download_path = os.getcwd() + os.sep +"download"
    file_name = download_path + os.sep + name + '_{}.mp4'
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    for index, url in enumerate(url_list):
        res = requests.get(url)
        with open(file_name.format(index+1), 'wb') as f:
            f.write(res.content)
            f.flush()
        print("提示: {}_{}.mp4 下载完成".format(name, index+1))
    else:
        print("提示: {} 下载完成".format(name))
print('提示: execjs 与 Node js 不兼容\n')

host = 'http://api.sigujx.com'
api_url = 'https://api.sigujx.com/yunjx{}/api.php'
video_url = 'http://www.wasu.cn/Play/show/id/9654002?refer=sll'
name = 'ggg'

video_url = input('电影链接: ')
name = input('电影名称: ')

base_urls = ['https://api.bbbbbb.me/?url=',
             'https://api.sigujx.com/yunjx/?url=',
             'https://api.sigujx.com/?url=',
             'https://api.sigujx.com/v.php?url=']
base_url = base_urls[3]
base_url += video_url
api_num = ''

while True:
    data = {
        'id': video_url,
        'type':'auto',
        'siteuser':'',
        'md5':'',
        'hd':'',
        'lg':''
    }
    print('video_url:', video_url)
    print('base_url:', base_url)
    # 解决 frame 识别
    headers = {
        'referer': base_url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    r = requests.get(base_url, headers=headers)
    html = r.text
    if len(html) < 10000:
        break
    #print(r.text)
    if '"key":sigu' in html:
        sigu = getSiguStr(html)
        #print('sigu:', sigu)
        data['key'] = getSigu(sigu)
    hmd5 = getHmd5Str(html)
    #print('hmd5: {}'.format(hmd5))
    data['md5'] = getSign(hmd5)

    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'referer': base_url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    print('api_url: {}'.format(api_url.format(api_num)))
    print('data: {}'.format(data))
    r = requests.post(api_url.format(api_num), data=data)
    print('result:', r.json())
    print()
    if r.json()['ext'] == 'm3u8' or 'm3u8' in r.json()['url']:
        url_encoded = r.json()['url']
        url = parse.unquote(url_encoded)
        download_m3u8(url, name)
        break
    elif r.json()['ext'] == 'xml':
        r = requests.get(r.json()['url'])
        url_list = re.findall('<file><!\[CDATA\[(.*?)\]\]></file>', r.text)
        download_mp4(url_list, name)
        break
    else:
        video_url = 'http' + r.json()['url'].split('=http')[-1]
        if 'http' != r.json()['url'][:4:]:
            base_url = host + r.json()['url']
        else:
            base_url = r.json()['url']
    api_num = ''
    for i in r.json()['url'].split('/'):
        if 'yunjx' in i:
            api_num = i[5::]
    print()
    
