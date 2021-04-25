from selenium import webdriver
import time

Server=r'C:\Users\User\Desktop\Designing-implementing-and-testing-an-IoT-based-vital-signs-monitoring-system-for-elderly-health-ca\Code\Zenbo code\selenium\chromedriver.exe'
driver=webdriver.Chrome(Server)
driver.get('http://192.168.0.164:8000/qrcode')
time.sleep(20)