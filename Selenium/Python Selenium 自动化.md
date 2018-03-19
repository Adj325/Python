**说明: 这个笔记很多是个人总结, 当然也有些内容是先搜索后复制, 修改, 总结而来的.**

### 个人感受
折腾了selenium这么久, '所见即所得', 是我最大的体会了!
1. 呈现在网页的内容, 你都能通过selenium找到.
2. 你当前看到的, 就是你当前仅能操作的
	- 网页源代码page_source实时更新
	- 不可对不在网页上的元素进行操作
3. 框架frame是个坑, page_source仅是当前框架的源代码

### 常见问题

#### 01. 浏览网页登录, 登录框
- 解决方法:
http://username:password@the-site.com
#### 02. Screenshot: available via screen
- 无法找到元素
   -  使用phantomjs时, 未设置窗口大小, 导致元素不可见: 设置下窗口大小 

####  03. Element is not clickable at point(x, y). Other element would receive the click
- 无法点击元素, 否则将点击到别的元素
   -  元素被遮挡: 想法弄走遮盖元素, 或暂停一会让其自动消失
   -  元素未出现在窗口内: 下拉滚动条, 使元素出现
   -  元素未获得焦点: 使其获得焦点

#### 04. No such Frame 或 Unable to locate element
- 没有此框架 或 无法找到元素
   - 框架/元素未加载: 显式/隐式等待, 添加暂停
   - 元素在框架内: 切换到框架
   - 元素的定位不正确(动态id或class): 更改定位方法
   - 由于未知原因, 无法定位: 更换定位方法, xpath或css selector<br>
   补充: 从浏览器直接copy出来的xpath路径, 以前能用, 现在却不能用, 换为css却行了!<br>
初步怀疑是路径的问题, '/html/body/div/section/section[4]/div[2]/ul/li[4]', 由于对xpath的了解不够多, 所以尚未从根源上解决!
   - 动态路径: 根据网页内容, 动态更改路径

#### 05. element is not attached to the page
- 元素不在当前页面
   - 页面的刷新使元素对象发生改变: 重新定位元素
   - 元素归属于旧页面(另外一个url)的: 无解 

#### 06. send_keys报错
- 浏览器不兼容
   - 降低浏览器版本
- 接受体元素不对
   - 找到对应的接收体元素

#### 06. Compound class names not permitted
- 无法定位复合类(class="tile div")
   - 取其中独特的类名, 或使用其它定位方法

#### 07. page_source可见不可得
- 框架原因(page_source仅是显示当前框架的实时内容)
  - 切入更新的框架, 再取得它的page_source

### 常用函数
#### 01. 获取cookies
- cookie = driver.get_cookies()<br>
cookieList = ['{}={}'.format(item["name"], item["value"])  for item in cookie] <br> 
cookiestr = '; '.join(cookieList)<br>

#### 02. 获取网页源代码
- driver.page_source
注意, 网页源代码是实时更新的

#### 03. 获取当前网址
- driver.current_url 
注意, 网页网址是实时更新的

#### 04. frame框架切换
- 切换到id为child_frame的框架: driver.switchTo().frame("child_frame")<br>
切换回默认框架: driver.switchTo().defaultContent()<br>
框架的切换是一层一层, 由外到里的<br>
切进内框架后, 必须在**切回外框架**后, 才能对外框架的元素进行操作<br>
- 传入id、name、index以及selenium的WebElement对象来切换框架<br>
传入index时, 0指的是第一个子框架, 不是根框架!<br>
- 由于不可知原因, 对子框架进行操作时, 有时得多次切换回到默认框架, 再切进子框架, 然后才能对子框架进行操作<br>

#### 05. 获取标签属性
- tag.get_attribute(attributename)
a.get_attribute('href')

### 延时, 显/隐式等待
#### 01. time.sleep()
- 延时, 固定等待时长<br>
#### 02. Implicit Waits（隐式等待）
- 隐式等待是在尝试发现某个元素的时候，如果没能立刻发现，就==等待固定长度的时间==(默认为0秒)，等待完成后, 成功发现元素或抛出异常。一旦设置了隐式等待时间，它的作用范围就是Webdriver对象实例的整个生命周期。(修改自: 简书 半个王国)<br>
1.若无法成功找到元素, 就会等待固定时长后再去寻找<br>
2.默认0秒, 即: 找不到元素后, 没有等待时长, 于是不再寻找该元素, 直接抛出异常<br>
3.整个生命周期, 设置一次, 再程序结束前都有效<br>
隐式等待有时不好用, 程序执行很快, 但是浏览器, 网络很慢, 可能造成每个操作都要等待固定时长<br>
`driver.implicitly_wait(seconds)` 

#### 03. Explicit Waits（显式等待）
 - 对于特定元素, 指定某个条件，然后设置最长等待时间。在这个时间内不断尝试寻找元素，找不到便会抛出异常。只有该条件触发，才执行后续代码。
1.特定元素, 针对不是所有元素
2.某个条件, 对于不同元素有不同的等待条件

 - WebDriverWait(driver=driver, timeout=300, poll_frequency=0.5,  ignored_exceptions=None).until(EC.xx((By.xx, 'xx')))
driver：浏览器驱动
timeout：最长超时等待时间(s)
poll_frequency：检测的时间间隔，默认为500ms
ignore_exception：超时后抛出的异常信息，默认情况下抛 NoSuchElementException 异常

 - until() 或者 until_not()
until(method, message='')
调用该方法体提供的回调函数作为一个参数，直到返回值为True
until_not(method, message='')
调用该方法体提供的回调函数作为一个参数，直到返回值为False

 - WebDriverWait(driver, timeout).until(EC.xx((By.xx,  "xx")))
 - EC: 预期条件
title_is：判断当前页面的title是否等于预期<br>
title_contains：判断当前页面的title是否包含预期字符串<br>
presence_of_element_located：判断某个元素是否被加到了dom树里，并不代表该元素一定可见<br>
visibility_of_element_located：判断某个元素是否可见. 可见代表元素非隐藏，并且元素的宽和高都不等于0<br>
visibility_of：跟上面的方法做一样的事情，只是上面的方法要传入locator，这个方法直接传定位到的element就好了<br>
presence_of_all_elements_located：判断是否至少有1个元素存在于dom树中。举个例子，如果页面上有n个元素的class都是'column-md-3'，那么只要有1个元素存在，这个方法就返回True<br>
text_to_be_present_in_element：判断某个元素中的text是否包含了预期的字符串<br>
text_to_be_present_in_element_value：判断某个元素中的value属性是否包含了预期的字符串<br>
frame_to_be_available_and_switch_to_it：判断该frame是否可以switch进去，如果可以的话，返回True并且switch进去，否则返回False<br>
invisibility_of_element_located：判断某个元素中是否不存在于dom树或不可见<br>
element_to_be_clickable - it is Displayed and Enabled：判断某个元素中是否可见并且是enable的，这样的话才叫clickable<br>
staleness_of：等某个元素从dom树中移除，注意，这个方法也是返回True或False<br>
element_to_be_selected：判断某个元素是否被选中了,一般用在下拉列表<br>
element_located_to_be_selected<br>
element_selection_state_to_be：判断某个元素的选中状态是否符合预期<br>
element_located_selection_state_to_be：跟上面的方法作用一样，只是上面的方法传入定位到的element，而这个方法传入locator<br>
alert_is_present：判断页面上是否存在alert<br>

- By: 定位方式 

实际使用中, 发现显/隐式等待, 对Python环境自带的IDE, 支持不好; 用pycharm执行不会报错, 用自带的就遇到了很多问题.

### 常用js操作
#### 01. js下拉滚动条
- 移动到元素element对象的“顶端”与当前窗口的“顶部”对齐  
driver.execute_script("arguments[0].scrollIntoView();", element);  
driver.execute_script("arguments[0].scrollIntoView(true);", element);  

- 移动到元素element对象的“底端”与当前窗口的“底部”对齐  
driver.execute_script("arguments[0].scrollIntoView(false);", element);  

- 移动到页面最底部  
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");  

- 移动到指定的坐标(相对当前的坐标移动)
driver.execute_script("window.scrollBy(0, 700)");   
结合上面的scrollBy语句，相当于移动到700+800=1600像素位置  
driver.execute_script("window.scrollBy(0, 800)");  

- 移动到窗口绝对位置坐标，如下移动到纵坐标1600像素位置  
driver.execute_script("window.scrollTo(0, 1600)");  
- 结合上面的scrollTo语句，仍然移动到纵坐标1200像素位置  
driver.execute_script("window.scrollTo(0, 1200)");

- 移动到指定元素(根据**css选择器**定位)
driver.execute_script('''$('html,body').animate({scrollTop:$(css选择器位置).offset().top}, 800);''')

#### 02. js 构造表单实现提交
``` javascript
 function post(URL, PARAMS) {
	var temp_form = document.createElement("form");
	temp_form.action = URL;
	temp_form.target = "_self";
	temp_form.method = "post";
	 temp_form.style.display = "none";
	for (var x in PARAMS) {
		var opt = document.createElement("textarea");
		opt.name = x;
 		opt.value = PARAMS[x];
		temp_form.appendChild(opt);
	}
	document.body.appendChild(temp_form);
	temp_form.submit();
}
post('register', {'name':'nidaye', 'pwd':'hello'});
```
#### 03. js 其它操作
- 关闭当前窗口
window.close();

### 某个关于Element is not clickable at point的issue
[Chrome - Element is not clickable at point · Issue #2766 · SeleniumHQ/selenium-google-code-issue-archive](
https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/2766)
