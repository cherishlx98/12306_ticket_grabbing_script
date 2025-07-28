import platform
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 读取配置文件信息
def load_setting():
    try:
        with open('settings.txt', 'r') as file:
            settings={}
            for line in file:
                key, value = line.strip().split('=', 1)
                settings[key] = value
        return settings
    except Exception:
        print('打开文件出错')
        return None

settings = load_setting()

# 获取浏览器驱动
def get_driver():
    # 判断当前操作系统，选择对应的浏览器驱动程序
    system = platform.system()

    # 浏览器驱动路径
    path = ''
    if system == 'Windows':
        path = 'chromedriver/chromedriver.exe'
        print("当前操作系统：Windows")
    elif system == 'Darwin':
        path = 'chromedriver/chromedriver'
        print("当前操作系统：macOS")
    else:
        print(f"未知操作系统：{system}")
        return None
    service = Service(executable_path=path)
    return webdriver.Chrome(service=service)

driver = get_driver()

# 去到12306登录页面
driver.get('https://kyfw.12306.cn/otn/resources/login.html')

# 法一：使用账号密码登录
def account_password_login():
    if 'username' not in settings or 'password' not in settings or 'last4' not in settings:
        print('settings配置文件中username,password出错，请仔细检查')
        driver.quit()
        # exit(0)：表示程序成功执行并正常退出
        # exit(1)（或任何非零值）：表示程序因错误或异常情况而终止
        exit(1)

    # .login-hd-code 选择所有class包含login-hd-code的节点
    driver.find_element(By.CSS_SELECTOR, '.login-hd-code').click()
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, '#J-userName').clear()
    driver.find_element(By.CSS_SELECTOR, '#J-userName').click()
    driver.find_element(By.CSS_SELECTOR, '#J-userName').send_keys(settings['username'])
    driver.find_element(By.CSS_SELECTOR, '#J-password').clear()
    driver.find_element(By.CSS_SELECTOR, '#J-password').click()
    driver.find_element(By.CSS_SELECTOR, '#J-password').send_keys(settings['password'])

    driver.find_element(By.CSS_SELECTOR, '#J-login').click()
    # 这个框是新出现的，必须要等待它显示出来才能操作！！！
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, '#id_card').clear()
    driver.find_element(By.CSS_SELECTOR, '#id_card').click()
    driver.find_element(By.CSS_SELECTOR, '#id_card').send_keys(settings['last4'])

    driver.find_element(By.CSS_SELECTOR, '#verification_code').click()
    verification_code = input('请输入手机上收到的验证码：')
    driver.find_element(By.CSS_SELECTOR, '#code').clear()
    driver.find_element(By.CSS_SELECTOR, '#code').click()
    driver.find_element(By.CSS_SELECTOR, '#code').send_keys(verification_code)

    driver.find_element(By.CSS_SELECTOR, '#sureClick').click()

# 法二：扫码登录
def scan_code_login():
    driver.find_element(By.CSS_SELECTOR, '.login-hd-account').click()
    time.sleep(0.5)
    input('请手动完成扫码验证，然后按下回车键继续...')

# 1.实现登录逻辑
flag = input('请选择登录的方式，输入1（账号密码登录），2（扫码登录）:')

if flag == '1':
    account_password_login()
elif flag == '2':
    scan_code_login()
else:
    print('请检查输入是否正确，并重试～')
    exit(1)

print('账号登录成功')
time.sleep(2)

# 跳转到车票预订页面
# 2.实现预订座位
driver.find_element(By.CSS_SELECTOR,'#link_for_ticket').click()
time.sleep(1)
# 选择单程
driver.find_element(By.CSS_SELECTOR,'#dc').click()
driver.find_element(By.CSS_SELECTOR,'#fromStationText').clear()
driver.find_element(By.CSS_SELECTOR,'#fromStationText').click()
driver.find_element(By.CSS_SELECTOR,'#fromStationText').send_keys(settings['fromStationText'])
driver.find_element(By.CSS_SELECTOR, '#fromStationText').send_keys(Keys.ENTER)
driver.find_element(By.CSS_SELECTOR,'#toStationText').clear()
driver.find_element(By.CSS_SELECTOR,'#toStationText').click()
driver.find_element(By.CSS_SELECTOR,'#toStationText').send_keys(settings['toStationText'])
driver.find_element(By.CSS_SELECTOR,'#toStationText').send_keys(Keys.ENTER)
driver.find_element(By.CSS_SELECTOR,'#train_date').clear()
driver.find_element(By.CSS_SELECTOR,'#train_date').click()
driver.find_element(By.CSS_SELECTOR,'#train_date').send_keys(settings['train_date'])
# 选择sf1普通票，sf2学生票
passenger_type = settings['passenger_type']
if passenger_type == '普通':
    driver.find_element(By.CSS_SELECTOR,'#sf1')
elif passenger_type == '学生':
    driver.find_element(By.CSS_SELECTOR,'#sf2')
else:
    print('未知乘客类型，请仔细检查配置文件')
    exit(1)

driver.find_element(By.CSS_SELECTOR,'#sf1').click()
# TODO 等待到开抢时间，12306一般提前15天开售
time.sleep(0.5)
driver.find_element(By.CSS_SELECTOR,'#query_ticket').click()

# 选择器 #queryLeftTable tr:nth-child(1) .btn72 可以分解为：
# queryLeftTable：查找 ID 为 queryLeftTable 的元素（通常是表格）
# tr:nth-child(1)：在该表格中查找第一个 <tr> 行元素
# .btn72：在该行中查找 class 包含 btn72 的元素
time.sleep(1)
driver.find_element(By.CSS_SELECTOR,'#queryLeftTable tr:nth-child(1) .btn72').click()

time.sleep(0.5)
driver.find_element(By.CSS_SELECTOR,'#normalPassenger_0').click()

driver.find_element(By.CSS_SELECTOR,'#submitOrder_id').click()
time.sleep(0.5)
driver.find_element(By.CSS_SELECTOR,'#qr_submit_id').click()
print('已提交订单，请在12306官网或APP完成支付')

# 关闭浏览器
driver.quit()