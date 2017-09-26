from bs4 import BeautifulSoup
import requests
import lxml.html
import webbrowser
import time
import re

URL = "https://byuh.instructure.com/login/ldap"
s= requests.session()

def parser(date, td_list):
	result = []
	for td in td_list:
		for elem in td:
			if elem.p is not None:
				text = elem.p.text.encode('utf-8','replace')
				text = text.replace(' ', '')
				if "Sep12" in text.strip():
					print text
		print "----------------------------"
	
def scraper():
	login = s.get(URL)
	login_html = lxml.html.fromstring(login.text)
	hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
	form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
	form['pseudonym_session[unique_id]'] = "jwoff25"
	form['pseudonym_session[password]'] = "Majidelife25"
	response = s.post(URL, form)

    #webbrowser.open(response.url)
	result = s.get("https://byuh.instructure.com/courses/1458536")
	rel_page = result.content
	page = BeautifulSoup(rel_page,"lxml")
	table = page.find_all('table')
	check = []
	for tr in table[3].find_all('tr'):
		tmp = []
		for td in tr.find_all('td'):
			tmp.append(td)
		check.append(tmp)
	parser("Tue, Oct 17", check)

if __name__ == '__main__':
	scraper()
