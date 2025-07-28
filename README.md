# 12306_ticket_grabbing_script
python使用selenium实现12306抢票脚本

### 前期环境搭建

Python版本：3.9+

Selenium版本：4.31+

谷歌浏览器驱动chromedriver（需区分Windows/Mac）：下载地址

克隆项目代码：

```shell
git clone https://github.com/cherishlx98/12306_ticket_grabbing_script.git
```

### 配置文件

在运行项目之前，找到项目目录下的settings.txt文件，按照自身12306账号情况进行修改

```
username=12306登录账号（用户名/邮箱/手机号）
password=12306密码
last4=身份证最后4位（如：0031）
fromStationText=出发地（如：永川东）
toStationText=目的地（如：重庆）
train_date=出发日（如：2025-08-08）
passenger_type=乘客类型（只有普通和学生，如：普通）
```



## 1.实现登录逻辑

1️⃣获取浏览器驱动



## 2.实现预订座位



## 3.实现支付提醒

## 4.后记
