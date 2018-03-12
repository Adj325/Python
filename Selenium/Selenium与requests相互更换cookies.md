### selenium获取cookies给requests
``` python
# 登录后, 从selenium中获取cookies
cookies = browser.get_cookies()
``` 
- 法一: session
``` python
# 创建一个session的请求对象
s = requests.session()
# 遍历
for cookie in cookies:
    s.cookies.set(cookies['name'], cookies['value'])
```
- 法二: header
``` python
# 请求头中cookies键的值
cookiestr = ''
# 连接有效cookies值
for cookie in cookies:
    cookiestr = cookiestr + cookies['name'] + '=' + cookies['value'] + ';' + ' '
headers['cookies'] = cookiestr
```

### requests获取cookies给selenium

``` python
# 创建一个session的请求对象
session = requests.session()
....
cookies = session.cookies
cookiesstr = '; '.join(['='.join(item) for item in cookies.items()])
```
