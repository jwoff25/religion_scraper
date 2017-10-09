from bs4 import BeautifulSoup
import requests
import lxml.html
import webbrowser
import time
import re
import os

URL = "https://byuh.instructure.com/login/ldap"
s= requests.session()
	
def scraper():
	login = s.get(URL)
	login_html = lxml.html.fromstring(login.text)
	hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
	form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
	user_id = raw_input("Enter username: ")
	pswd = raw_input("Enter password: ")
	form['pseudonym_session[unique_id]'] = user_id
	form['pseudonym_session[password]'] = pswd
	response = s.post(URL, form)

    #webbrowser.open(response.url)
	result = s.get("https://byuh.instructure.com/courses/1458536")
	rel_page = result.content
	page = BeautifulSoup(rel_page, "lxml")
	table = page.find_all('table')
	check = []
	with open("scriptures.txt", 'w') as file:
		for tr in table[3].find_all('tr'):
			flag = False
			for td in tr.find_all('td'):
				if td.p is not None:
					if re.match("^Tue.|^Thu.", td.p.text):
						flag = True
					if flag == True:
						p_text = td.find_all('p')
						for p in p_text:
							file.write(p.text.encode('utf-8', 'replace') + "|")
							#if p.a is not None:
								#file.write(p.a['href'].encode('utf-8', 'replace') + "|")
								
						
			file.write("\n")

if __name__ == '__main__':
	scraper()
