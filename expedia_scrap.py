# -*- coding: utf-8 -*-
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import codecs

review = []
date = []
rating = []

def get_response_from_server(url):
	try:
		cnt = 0
		browser = webdriver.Chrome()
		browser.get(url)
		browser.find_element_by_xpath('.//*[@id="link-to-reviews"]').click()
		wait = WebDriverWait(browser, 13)

		while(True):
			
			time.sleep(15)
			cnt += 1
			# store it to string variable
			page = browser.page_source
			soup=BeautifulSoup(page, 'html.parser')
			scrap_logic(soup)

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

def scrap_logic(soup):
	#soup = BeautifulSoup(open("expedia.html"), "html.parser")
	flag = True
	detail = soup.find_all('div', {'class': 'details'})
	dt = soup.find_all('div', {'class': 'date-posted'})
	x = 0
	for tag in detail:
		#print "here"
		rvtxt = tag.find('span', {'class': 'translate-text'})
		if rvtxt == None:
			x += 1
			continue
		review.append(rvtxt.get_text())
		
		rtsc = tag.find('span', {'class': 'badge badge-notification rating-score left'})
		rating.append(rtsc.get_text())

		tmp = dt[x].get_text().split()
		date.append(' '.join(word for word in tmp))
		x += 1

url = "https://www.expedia.co.in/Ooty-Hotels-Kurumba-Village-Resort.h6129303.Hotel-Information?chkin=29%2F05%2F2018&chkout=30%2F05%2F2018&rm1=a2&hwrqCacheKey=f7945c2a-d72b-462c-a6af-254594b327a2HWRQ1527593270029&cancellable=false&regionId=6234125&vip=false&c=a3c473ef-ac7b-400f-a1ab-82c2b0d7b8d0&&exp_dp=13409.93&exp_ts=1527593245227&exp_curr=INR&swpToggleOn=false&exp_pg=HSR"
get_response_from_server(url)

#scrap_logic("abc")

print ("Total reviews are")
print (len(review), len(date))

with codecs.open("output.txt", "w", encoding="utf-8") as thefile:
	for x in range(len(review)):
		thefile.write("%s\n" % date[x].decode("utf-8"))
		thefile.write("%s\n" % rating[x].decode("utf-8"))
		thefile.write("%s\n\n" % review[x].decode("utf-8"))
thefile.close()