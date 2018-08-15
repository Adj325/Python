# 漫画下载

- 爬取网站

  1. [极速漫画](http://tel.1kkk.com)

  2. [乙女漫画](http://www.nokiacn.net/)

- 过程分析

  图片是采用ajax获取的，各采用不同反爬策略。

  分析后，有以下结论。

  **1. 乙女漫画**

    关键js：http://www.nokiacn.net/template/skin2/css/d7s/js/show.20170501.js?20180620083618

    关键变量：qTcms_S_m_murl_e，qTcms_S_m_murl

    调试方法：复制js内容到pycharm，不断删减灰色无用字段，最后找到qTcms_S_m_murl及qTcms_S_m_murl_e

    数据获取过程：访问到某漫画的某章节后，后端会把该章节的所有照片链接拼接起来，然后通过base64加密，并把加密后的字符串返回给前端。

  **2. 极速漫画**

    关键js：http://css99tel.cdndm5.com/v201808091405/blue/js/chapternew_v22.js

    关键方法：ajaxloadimage()

    关键变量：DM5_*

    数据获取过程：访问到某漫画的某章节后，后端会返回一个DM5密钥，使用此密钥访问chapterfun.ashx会得到一段混淆后的js，执行后得到两张图片(当前页与下一页)的下载链接。

    难点：需要使用session，需要动态变化headers，js的获取链接只能拼接(data=data，会获取不到脚本;data=data不行，可能是因为没把/及空格给转码。)，js的执行需要调用selenium（execjs及pyv8都不行）。

    > PS：不直接使用selenium，主要是因为打开漫画首页会持续加载，不会自行停止。selenium的控制也是较麻烦的。

- 最后

  是为了看《徒然喜欢你》才写的脚本的，在爬取其他漫画时，有些细节也许需要自行修改。

     
