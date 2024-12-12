# coding = utf-8
from selenium import webdriver #
import time,sys,ddddocr
#from selenium.webdriver.common.alert import Alert
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver import firefox
#from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import TimeoutException


options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/4.0 (compatible;MSIE 8.0;Windows NT 6.1;Trident/4.0)"')
driver = webdriver.Chrome(chrome_options = options)


# 配置文件地址
#profile_directory = (r'C:\Users\hp\AppData\Roaming\Mozilla\Firefox\Profiles\k0rf4iuy.default')
# 加载配置配置
#profile = webdriver.FirefoxProfile(profile_directory)
# 启动浏览器配置
#driver = webdriver.Firefox() # copy geckodriver.exe to python dir PPT
#driver = webdriver.Ie()
#driver = webdriver.Chrome() # copy driver.exe to python dir video
u=2014006046
#p=960761
p='lilei@1979'
#u=2014005976
#p=822400
i=0 # 是否登录标志
t=0 # 学习累计时间
kc='必修课'

driver.maximize_window() # 浏览器最大化
#driver.minimize_window() # 浏览器最小化
#driver.implicitly_wait(6) # 隐性等待

def login(username,password): # 登录
    driver.get('https://www.lngbzx.gov.cn/pc/index.html#/') # 登录页面
    time.sleep(1) # 强制等待
    driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/form[1]/div[1]/div/div/input').send_keys(username) # 用户名
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/form[1]/div[2]/div/div/input').send_keys(password) # 密码
    time.sleep(1)

    img = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/form[1]/div[3]/div/img')
    data = img.screenshot_as_png
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(data)
    print(res)

    driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/form[1]/div[3]/div/div/input').send_keys(res) # 验证码
    time.sleep(2)
    clkbtn = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/form[1]/div[4]/div/button') # 获取登录按钮
    #clkbtn.click()
    #ActionChains(cls.driver).move_to_element(clkbtn).click().perform()
    driver.execute_script("arguments[0].click();", clkbtn)# 点击登录按钮
    time.sleep(3)

def loading(sj): # 显示学习进度，3秒更新一次
    for n in range(0,60,1):
        sys.stdout.write('#' * (n+1) + '.' * (60-n-1) + '  '+ str((n+1)*100//60) + '%\r')
#       sys.stdout.flush()
        time.sleep(sj/60)
    sys.stdout.write('\n')


# 判断是否登录成功

while i == 0:
    login(u,p)
    #print('登录成功')
    #i=1
    #time.sleep(2)


    myname = driver.find_elements_by_xpath(f"//*[contains(text(), '李雷')]")
    if myname:
        print('登录成功')
        i=1
        time.sleep(2)
    else:
        print('系统失败')
        time.sleep(2)

'''
    if driver.current_url != 'https://lngbzx.gwypx.com.cn/pc/index.html#/study_center/my_course': # 登录成功，进入学习中心
        print('系统失败')
        time.sleep(2)
    else:
        print('登录成功')
        i=1
        time.sleep(2)
'''

driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[1]').click() # 点击学习中心
time.sleep(3)
driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/ul/li[2]').click() # 点击我的课程

first=driver.current_window_handle # 获取当前窗口句柄
print('first window is',first) # 输出当前窗口句柄
#driver.find_element_by_id("top-mycourse").click() # 进入课程
time.sleep(3)
#driver.find_element_by_link_text(kc).click() # 选择必修/选修课
#driver.find_element_by_link_text("课程").click()
time.sleep(3)
while i != 0:
    try:
        #driver.find_element_by_class_name("course_play").click() # 点击播放按钮
        driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div/div[2]/div[3]/div/ul/li[1]/div[1]/div/div[2]/div[4]/div[2]/div/div[1]').click()
    except:
        kc = '选修课'
        print('begin to study',kc)
        driver.find_element_by_link_text(kc).click() # 选择必修/选修课
        time.sleep(3)
        driver.find_element_by_class_name("course_play").click() # 点击播放按钮
    else:
        print('begin to study',kc)
    time.sleep(3)
    handles = driver.window_handles # 获取当前全部窗口句柄集合
    print ('handles is',handles) # 输出句柄集合
    for handle in handles:# 切换窗口
        if handle != first:
            print('switch to second window',handle)
            driver.switch_to.window(handle) #切换到第二个窗口
            print('switch to second window ok')
            try:
                #driver.switch_to.frame("courseplay")#切换iframe
                stdbtn = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[5]/div/div[3]/span/button') #点击开始学习
                driver.execute_script("arguments[0].click();", stdbtn)
            except:
                print("没有开始学习按钮")
            else:
                print("有开始学习按钮")
            #driver.execute_script("jQuery.fx.off=true")
            #driver.find_Element_by_xpath("//input[@class='alert']").click()
            #WebDriverWait(driver, 3).until(EC.alert_is_present())
            #alert = driver.switch_to.alert
            #alert.accept()
            '''
            if EC.alert_is_present:
                print(EC.alert_is_present)
                print("Alert exists")
                time.sleep(2)
             #   driver.send_keys(Keys.SPACE)
                alert = driver.switch_to_alert()
                time.sleep(2)
                print('ok---')
                print (alert.text)
                alert.accept()
                print("Alert accepted")
            else:
                print("NO alert exists")
#            t = driver.switch_to.alert
#            print('find alert')
#            time.sleep(1)
#            print(t.text)
#            t.dismiss()
           '''
            '''
            try: # 异常处理
                t = driver.switch_to_alert() # 处理浏览器版本对话框
                print(t.text)
                t.accept()
            except:
                print('This is a video.')
            else:
                print('This is a ppt.')
            time.sleep(5)
            #driver.switch_to.frame() # 进入frame
            #driver.find_element_by_partial_link_text("进入课程").click() # iframe结构，开始学习，不影响计时
            #time.sleep(180)
            '''
            loading(180) # 180秒为一个计时周期
            driver.close() # 关闭第二个窗口
            t = t + 1
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))# 输出当前时间
            print('total study',t*3//60,'hour',t*3%60, 'minute.')# 学习时间
            print('switch to first window',first)
            driver.switch_to.window(first) #切换回第一个窗口
    time.sleep(2)
    driver.refresh() # 刷新页面
    #driver.find_element_by_link_text(kc).click() # 通过选择必修/选修刷新页面
    time.sleep(3)

#http://gwy.lngbzx.gov.cn/login.jsp?error=true # 密码错误
#http://gwy.lngbzx.gov.cn/system_busy.jsp # 系统繁忙
#http://gwy.lngbzx.gov.cn/student/index.do # 登录成功，进入学习中心
