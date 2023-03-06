import csv
from selenium import webdriver
from time import sleep
from langdetect import detect
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as bs
import undetected_chromedriver as uc
from selenium.webdriver.firefox.options import Options

def create_driver(headless=True):
	options = uc.ChromeOptions()
	options.headless=headless
	options.add_argument("--window-size=1920,1080")
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--allow-running-insecure-content')
	options.add_argument('--headless')

	driver = uc.Chrome(use_subprocess=True, options=options)
	
	driver.set_page_load_timeout(15)
	
	return driver

def get_page(url,driver):
	driver.get(url)
	test(driver.page_source,'test.html')

def test(content,name,mode='a'):
	with open(name,mode,encoding='utf-8') as f:
		f.write(content)

def csv_pack(name,params,mode='a+'):		
	with open(name + '.csv',mode,newline='',encoding='utf-8-sig') as file:
		writer = csv.writer(file,delimiter=',')
		writer.writerow(params)


def analysis(site,driver):
	driver.get('https://'+site)
	sleep(10)
	if len(driver.page_source) < 1000:
		lang = 'NA'
	else:
		lang = detect(bs(driver.page_source,'html.parser').text)
	return lang

def parse():
	driver = create_driver()

	with open('sites.txt','r') as file:
		sites = file.read().splitlines()

	count = 0
	for site in sites:
		print(site)
		if count == 15:
			count = 0
			driver.close()
			driver = create_driver()

		while True:
			try:
				lang = analysis(site,driver)
				csv_pack('result',[site,lang])
				count+=1
				break
			except:
				continue
parse()