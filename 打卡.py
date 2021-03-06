from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import datetime
import time
import win32api,win32con

path_init = os.path.dirname(os.path.realpath(__file__))

def get_up():	#获取用户名和密码
	with open(path_init + '\\用户名和密码.txt', 'r', encoding = 'utf-8') as f:
		content = f.read()
	content_list = content.split('：')

	username = content_list[1].split( )[0]
	password = content_list[2]
	return username, password

def connection():	#判断网络是否连接
	exit_code = os.system('ping www.baidu.com')
	if exit_code:	#网络连通 exit_code == 0，否则返回非0值。
		win32api.MessageBox(0, '请检查你的网络连接，30秒后重试', '警告', win32con.MB_OK)
		raise Exception('connect failed.')

def main():
	driver = webdriver.Chrome(executable_path = r'D:\anaconda\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe')   # 声明一个浏览器对象   指定使用chromedriver.exe路径
	username, password = get_up()#获取用户名和密码

	url = 'https://ehall.jlu.edu.cn/infoplus/form/BKSMRDK/start'
	driver.get(url)  # 打开Chrome

	wait = WebDriverWait(driver, 5)

	input_username = wait.until(EC.presence_of_element_located((By.ID, 'username'))) # 显式等待通过id定位到input框
	input_username.send_keys(username)   # 在输入框内输入用户名
	input_password = driver.find_element_by_id('password')  # 通过id定位到input框
	input_password.send_keys(password)   # 在输入框内输入密码

	button_log_in = driver.find_element_by_id('login-submit')  # 获取登录按钮
	button_log_in.click()  # 点击登录

	driver.implicitly_wait(5)#隐式等待5秒

	radio_button_2 = driver.find_element_by_css_selector('[for="V1_CTRL28"]')# 获取正常按钮
	radio_button_2.click()  # 点击正常

	button_hand_in = driver.find_element_by_css_selector('.commandBar [class="command_button_content"]')  # 获取提交按钮
	button_hand_in.click()  # 点击提交

	driver.implicitly_wait(5)#隐式等待5秒

	button_good = driver.find_element_by_css_selector('.dialog_footer button')  # 获取好按钮
	button_good.click()  # 点击好

	driver.implicitly_wait(5)#隐式等待5秒

	button_ok = driver.find_element_by_css_selector('[class="dialog_button default fr"]')  # 获取确定按钮
	button_ok.click()  # 点击确定

	driver.implicitly_wait(5)#隐式等待5秒

	driver.close()      # 关闭浏览器

sign_in_morning = False
sign_in_night = False

if __name__ == '__main__':
	while True:
		time_now = datetime.datetime.now()
		print(time_now.hour)
		if not 7 <= time_now.hour <= 11 and not 21 <= time_now.hour <= 23:
			print('当前不在打卡时段')
			if 0 <= time_now.hour <= 6:
				win32api.MessageBox(0, '当前不在打卡时段\n距离打卡时间还有'+str(7 - time_now.hour)+'小时'+str(60 - time_now.minute)+'分钟', '提示', win32con.MB_OK)
				time.sleep((7 - time_now.hour - 1) * 60 * 60 + (60 - time_now.minute + 1) * 60)
			if 12 <= time_now.hour <= 20:
				win32api.MessageBox(0, '当前不在打卡时段\n距离打卡时间还有' + str(21 - time_now.hour) + '小时' + str(60 - time_now.minute) + '分钟', '提示', win32con.MB_OK)
				time.sleep((21 - time_now.hour - 1) * 60 * 60 + (60 - time_now.minute + 1) * 60)
		if 7 <= time_now.hour <= 11:
			sign_in_morning = True
			if sign_in_morning == True and sign_in_night == False:
				try:
					connection()
					main()
					sign_in_morning = False
					sign_in_night = True
					print('早打卡完成')
					win32api.MessageBox(0, '早打卡完成，完成时间：' + str(time_now), '提示', win32con.MB_OK)
					time.sleep(5*60*60)
				except:
					time.sleep(30)
		elif 21 <= time_now.hour <= 23:
			sign_in_night=True
			if sign_in_night == True and sign_in_morning == False:
				try:
					connection()
					main()
					sign_in_morning = True
					sign_in_night = False
					print('晚打卡完成')
					win32api.MessageBox(0, '晚打卡完成，完成时间：' + str(time_now), '提示', win32con.MB_OK)
					time.sleep(3*60*60)
				except:
					time.sleep(30)
		else:
			print(time_now)
			time.sleep(60)
