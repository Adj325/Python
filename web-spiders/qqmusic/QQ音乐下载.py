import requests
search_url = '''http://soso.music.qq.com/fcgi-bin/search_cp?aggr=0&catZhida=0&lossless=1&sem=1&w={}&n=15&t=0&p=1&remoteplace=sizer.yqqlist.song&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=GB2312&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'''
headers = {
    "Host": "soso.music.qq.com",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'}
search_data = {
    'aggr':'0',
    'catZhida':'0',
    'lossless':'1',
    'sem':'1',
    'w':'',
    'n':'15',
    't':'0',
    'p':'1',
    'remoteplace':'wo.shi.nidaye',
    'g_tk':'5381',
    'loginUin':'0',
    'hostUin':'0',
    'format':'json',
    'inCharset':'GB2312',
    'outCharset':'utf-8',
    'notice':'0',
    'platform':'yqq',
    'needNewCode':'0'
    }

html = '''
<html>
<meta charset="utf-8">
<body>
{}
</body>
</html>

'''

def getStatusCode(url):
    try:
        url = url.replace('/', '%2F').replace('&', '%3F').replace('=', '%3D')
        headers = {
        "Host": "pl.soshoulu.com",
        'Referer':'http://pl.soshoulu.com/webspeed.aspx',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
        }
        url = 'http://pl.soshoulu.com/ajax/shoulu.ashx?_type=webspeed&url={}&px=1'.format(url)

        r = requests.get(url, headers=headers, timeout=1)
        return r.text.split('$')[0]
    except:
        return ''

print('关闭程序: CTRL+C')
while True:
    key = input('关键词: ')

    s = '<h1>关键词: {}</h1>'.format(key)
    
    headers['Host'] = 'soso.music.qq.com'
    session = requests.session()
    r = session.get(search_url.format(key), data=search_data, headers=headers)

    li = r.json()['data']['song']['list']
    headers['Host'] = 'base.music.qq.com'
    for i, v in enumerate(li):
        print('{0:02d}: {1} - {2}, 专辑: {3}'.format(i+1, v['singer'][0]['name'], v['songname'], v['albumname']))
        guid = v['docid']
        songid = v['songmid']
        r = session.get('http://base.music.qq.com/fcgi-bin/fcg_musicexpress.fcg?json=3&guid={}'.format(guid), headers=headers)
        vkey = eval(r.text[13:-2:])['key']
        s += '<p>{0:02d}: '.format(i+1)
        flac_url = 'http://ws.stream.qqmusic.qq.com/F000{}.flac?vkey={}&guid={}&fromtag=53'.format(songid, vkey, guid)
        ape_url = 'http://ws.stream.qqmusic.qq.com/A000{}.ape?vkey={}&guid={}&fromtag=53'.format(songid, vkey, guid)
        mp3128_url = 'http://ws.stream.qqmusic.qq.com/M500{}.mp3?vkey={}&guid={}&fromtag=53'.format(songid, vkey, guid)
        mp3320_url = 'http://ws.stream.qqmusic.qq.com/M800{}.mp3?vkey={}&guid={}&fromtag=53'.format(songid, vkey, guid)
 
        if getStatusCode(flac_url) == '200':
            #print('flac: '+flac_url)
            s += ' <a href="{}">flac</a> '.format(flac_url)
        if getStatusCode(ape_url) == '200':
            #print('ape: '+ape_url)
            s += ' <a href="{}">ape</a> '.format(ape_url)
        if getStatusCode(mp3320_url) == '200':
            #print('320K: '+mp3320_url)
            s += ' <a href="{}">320K</a> '.format(mp3320_url)
        if getStatusCode(mp3128_url) == '200':
            #print('128K: '+mp3128_url)
            s += ' <a href="{}">128K</a> '.format(mp3128_url)

        print()
       
        s += ': {} - {}, 专辑: {}</p>'.format(v['singer'][0]['name'], v['songname'], v['albumname'])
        with open('预览.html', 'w', encoding='utf-8') as f:
            f.write(html.format(s))
