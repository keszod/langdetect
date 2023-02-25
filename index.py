import csv
from selenium import webdriver
from time import sleep
from langdetect import detect
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as bs
from selenium.webdriver.firefox.options import Options

def create_driver(headless=True):
	print('create_driver()')
	chrome_options = webdriver.ChromeOptions()
	if headless:
		chrome_options.add_argument("--headless")
	chrome_options.add_argument("--log-level=3")
	chrome_options.add_argument("--start-maximized")
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')
	chrome_options.add_argument('--disable-blink-features=AutomationControlled')

	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	chrome_options.add_experimental_option('useAutomationExtension', False)
	chrome_options.add_argument("--disable-blink-features")
	chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36")
	chrome_options.add_experimental_option("prefs", { 
	"profile.default_content_setting_values.media_stream_mic": 1, 
	"profile.default_content_setting_values.media_stream_camera": 1,
	"profile.default_content_setting_values.geolocation": 1, 
	"profile.default_content_setting_values.notifications": 1,
	"profile.default_content_settings.geolocation": 1,
	"profile.default_content_settings.popups": 0
  })
	
	caps = DesiredCapabilities().CHROME

	caps["pageLoadStrategy"] = "none"
	
	driver = webdriver.Chrome(desired_capabilities=caps,chrome_options=chrome_options)	

	driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
 "source": """
	  const newProto = navigator.__proto__
	  delete newProto.webdriver
	  navigator.__proto__ = newProto		
	  """
})
	driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
	driver.implicitly_wait(30)

	#params = {
	#"latitude": 55.5815245,
	#"longitude": 36.825144,
	#"accuracy": 100
	#}
	#driver.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
	#driver.refresh()
	
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