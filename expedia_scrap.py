from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

review = []
date = []
rating = []

def get_response_from_server(url):
	try:
		cnt = 0
		browser = webdriver.Chrome()
		browser.get(url)
		browser.find_element_by_xpath('.//*[@id="link-to-reviews"]').click()
		wait = WebDriverWait(browser, 10)
		
		while(True):
			
			time.sleep(7)
			cnt += 1
			# store it to string variable
			page = browser.page_source
			soup=BeautifulSoup(page, 'html.parser')
			scrap_result(soup)

			try:
				element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pagination-next')))
				print element
				element.click()
			except:
				break

	except Exception as e:
		print ("Error Occured")
		print (e)
		return

def scrap_result(soup):
	#soup = BeautifulSoup(open("expedia.html"), "html.parser")
	rev = soup.find_all('span', {'class':'translate-text'})
	for tmp in rev:
		review.append(tmp.get_text())

	dt = soup.find_all('div', {'class': 'date-posted'})
	for tmp in dt:
		date.append(tmp.get_text())

	rt = soup.find_all('span', {'class': 'badge badge-notification rating-score left'})	
	for tmp in rt:
		rating.append(tmp.get_text())

	for x in range(len(review)):
		print date[x], rating[x], review[x]

url = "https://www.expedia.co.in/Ooty-Hotels-Kurumba-Village-Resort.h6129303.Hotel-Information?chkin=29%2F05%2F2018&chkout=30%2F05%2F2018&rm1=a2&hwrqCacheKey=f7945c2a-d72b-462c-a6af-254594b327a2HWRQ1527593270029&cancellable=false&regionId=6234125&vip=false&c=a3c473ef-ac7b-400f-a1ab-82c2b0d7b8d0&&exp_dp=13409.93&exp_ts=1527593245227&exp_curr=INR&swpToggleOn=false&exp_pg=HSR"
get_response_from_server(url)

print ("Total reviews are")
print (len(review))