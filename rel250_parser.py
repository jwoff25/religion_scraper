import webbrowser
import time
import re
import os
import requests

def print_catalog(array):
	for c in array:
		print str(c[0]) + ": " + c[1]

def googler(queries):
	search_url = "http://www.google.com/search?q="
	for q in queries:
		webbrowser.open(search_url+q+"&btnI=1", new=1, autoraise = True)

def parser(user_input):
	src = catalog[user_input]
	src = src[3:]
	flags = ["due", "report", "exam"]
	search_queries = []
	for s in src:
		s = re.split("; |;", s)
		tmp = [x.split(",") for x in s if "," in x and re.search('\d+:\d+', x)]
		regex = re.compile(r'[a-zA-Z]+')
		for r in range(0,len(tmp)):
			book_name = re.findall(regex, tmp[r][0])
			s.remove(",".join(tmp[r]))
			for i in range(1,len(tmp[r])):
				tmp[r][i] = "".join(book_name) + tmp[r][i]
		s += [v for t in tmp for v in t]
		print s
		for i in range(0,len(s)):
			if not any(f in s[i] for f in flags):
				if re.search(regex, s[i]):
					bookname = re.findall(regex, s[i])
				else:
					s[i] = "".join(bookname) + " " + s[i]
				temp = s[i] + " lds"
				temp = temp.replace("D&C", "Doctrine and Covenants")
				search_queries.append(temp.replace(" ", "+"))
	googler(search_queries)
	print search_queries
	

if __name__ == "__main__":
	file = open("scriptures.txt", 'r')
	output_file = open("test.txt", 'w')
	catalog = []
	i = 0
	for line in file:
		if re.match("^[a-zA-z]", line):
			line = line.decode('unicode_escape').encode('ascii','ignore')
			arr = [i] + [w for w in line.strip().split("|") if w != ""]
			catalog.append(arr)
			i+=1
	print_catalog(catalog)
	usr_inp = int(raw_input("Enter ID: "))
	parser(usr_inp)
