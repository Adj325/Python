import os
import re
import time
import requests
from selenium import webdriver

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'tel.1kkk.com',
    'Upgrade-Insecure-Requests': '1'
}


class JiSuManHua:
    def __init__(self):
        self.s = requests.session()
        self.br = webdriver.Chrome()
        self.br.get('https://www.jianshu.com')

    def crawl(self, main_url, start=0):

        # 打开漫画所在页面，以初始化session
        main_rep = self.s.get(main_url, headers=headers)

        # 获取漫画名字
        manhua_name = re.findall('var DM5_COMIC_MNAME="(.*?)"', main_rep.text)[0]
        print('漫画名：{}'.format(manhua_name))

        # 以漫画名创建目录
        if not os.path.exists(manhua_name):
            os.mkdir(manhua_name)

        # 提取章节名及其url
        result_list = re.findall(
            '<li> {48}<a href="(.*?)" title="" target="_blank" >(.*?) {21}<span>(.*?)</span> {17}</a> {44}</li>',
            main_rep.text) + re.findall('<li><a href="(.*?)" title=".*?" target="_blank" >(.*?)<span>(.*?)</span>',
                                        main_rep.text)
        result_list = result_list[start::]

        print('提示：共{}话！\n'.format(len(result_list)))
        # 遍历解析所有章节
        for chapter_id, chapter_name, chapter_page_num in result_list:

            # 以章节名创建目录
            chapter_path = manhua_name + '/' + chapter_name.replace('/', " ")
            if not os.path.exists(chapter_path):
                os.mkdir(chapter_path)

            # 更改Host，以对应URL
            headers['Host'] = 'tel.1kkk.com'

            # 图片下载链接
            image_urls = []

            # 当前章节的页数/图片数
            chapter_page_num = re.findall('\d+', chapter_page_num)[0]
            chapter_page_num = int(chapter_page_num)

            print('提示："{}"，估计有{}张图片！'.format(chapter_name, chapter_page_num))

            # 按页码获取图片
            # 每次只有两个链接，所有需要执行多次，并更改page
            for page_id in range(chapter_page_num):
                # 补全章节链接
                chapter_url = 'http://tel.1kkk.com' + chapter_id + '#ipg{}'.format(page_id + 1)

                while True:
                    chapter_rep = self.s.get(chapter_url, headers=headers)

                    # 提取 关键信息，以获取图片下载链接
                    DM5_CID = re.findall('DM5_CID=(.*?);', chapter_rep.text)[0]
                    DM5_MID = re.findall('DM5_MID=(.*?);', chapter_rep.text)[0]
                    DM5_VIEWSIGN_DT = re.findall('DM5_VIEWSIGN_DT="(.*?)";', chapter_rep.text)[0]
                    DM5_VIEWSIGN = re.findall('DM5_VIEWSIGN="(.*?)";', chapter_rep.text)[0]
                    data = {
                        'cid': DM5_CID,
                        'page': page_id + 1,
                        'key': '',
                        'language': 1,
                        'gtk': 6,
                        '_cid': DM5_CID,
                        '_mid': DM5_MID,
                        '_dt': DM5_VIEWSIGN_DT,
                        '_sign': DM5_VIEWSIGN

                    }
                    s = ''
                    for key, val in data.items():
                        s += '{}={}&'.format(key, val)
                    s = s[:-1:]
                    s = s.replace(' ', '+')
                    s = s.replace(':', '%3A')
                    url = 'http://tel.1kkk.com/ch134-623820/chapterfun.ashx?{}'.format(s)

                    # 更改Host，以对应URL
                    headers['Host'] = 'tel.1kkk.com'
                    headers['Referer'] = 'http://tel.1kkk.com/{}/'.format(chapter_id)
                    img_rep = self.s.get(url, headers=headers)
                    if len(img_rep.text) > 2:
                        break

                # 构造脚本，调用浏览器执行，获取真正的图片的下载链接
                # 每次只有两个链接，所有需要执行多次，并更改page
                js = '''
                    function fun(){
                        body = $('body');
                        body.html();
                        li = '''
                js += img_rep.text + ''';
                        s = '';
                        for(var i=0; i<li.length; i++){
                            s += '<p>' + li[i] + '</p>';
                        }
                        body.html(s);
                        return s
                    }
                    fun()
                    '''
                self.br.execute_script(js)
                time.sleep(0.5)
                image_elements = self.br.find_elements_by_tag_name('p')

                # 提取图片下载链接
                for image_element in image_elements:
                    image_url = image_element.text
                    if image_url not in image_urls:
                        image_urls.append(image_url)
                        if len(image_urls) == chapter_page_num:
                            break

            # 下载当前章节图片到本地
            for image_url in image_urls:
                image_id = int(re.findall('/(\d+)_\d+\.\w+\?', image_url)[0])
                host_pre = re.findall('http://(.*?).cdndm5.com', image_url)[0]
                # 更改Host，以对应URL
                headers['Host'] = '{}.cdndm5.com'.format(host_pre)
                image_rep = self.s.get(image_url, headers=headers)

                if len(image_rep.content) < 4 * 1024:
                    print('下载"{}"时出现问题！'.format(image_url))

                with open('{0}/{1:03d}.jpg'.format(chapter_path, image_id), 'wb') as img:
                    img.write(image_rep.content)

            print('提示："{}"，成功下载{}张图片!\n'.format(chapter_name, len(image_urls)))

        else:
            print('\n漫画"{}"已爬取完毕！'.format(manhua_name))


manhua_url = 'http://tel.1kkk.com/manhua11839/'

JiSuManHua().crawl(manhua_url, 150)
