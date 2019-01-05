import requests
from threading import Thread
from bs4 import BeautifulSoup
from termcolor import cprint
import json
import re,time

class ProxyPools(Thread):
	def __init__(self, 
			intervalTime=120, debug=False,
			maxPoolSize=100,timeout=5):
		self.proxyList = []

		self.readPList = []
		self.respTimes = []

		self.killed = False
		self.timeSinceRun = int(time.time())
		self.intervalTime = intervalTime
		self.debug = debug
		self.maxPoolSize = maxPoolSize
		self.timeout = timeout
		Thread.__init__(self)

	def run(self):
		while not self.killed:
			if (int(time.time()) - self.timeSinceRun) % self.intervalTime == 0:
				if self.debug:	
					print ("...Starting Full Scrape...")
				self.timeSinceRun = int(time.time())
				self.initScrape()
			else:
				time.sleep(1)

	def getOne(self):
		if len(self.readPList) > 0:
			rtrnVal = self.readPList[0]
			self.readPList = self.readPList[1:]
			return rtrnVal
		else:
			raise ValueError('Empty List of Proxies')

	def getList(self):
		return self.readPList

	def getSize(self):
		return len(self.readPList)

	def initScrape(self):
		self.proxyList = []
		if self.debug:	
			print( "Scraping Site 1..."),
		self.site1() # works
		if self.debug:	
			print("done")
			print( "Scraping Site 2..."),
		self.site2() # works
		if self.debug:	
			print("done")
			print( "Scraping Site 3..."),
		self.site3() # works
		if self.debug:	
			print("done")
			print( "Scraping Site 4..."),
		self.site4() # works
		if self.debug:	
			print("done")
		if self.debug:	
			cprint("Succesfully added {} proxies!".format(len(self.proxyList)), 'green')
		self.proxyList = self.proxyList[::-1]
		self.filterConnections()

	def filterConnections(self):
		count = 0
		for proxy in self.readPList:
			if self.killed:
				break
			try:
				proxies = {
			  		'http': proxy,
			  		'https': proxy
				}
				r = requests.get("http://google.com", proxies=proxies, timeout=self.timeout)
				if(r.status_code == 200):
					#responseTime = r.elapsed.total_seconds()
					if self.debug:
						cprint("Still Working {0}! Reponse Time: {1}".format(proxy,responseTime),"green")
				else:
					del self.readPList[count]
					del self.respTimes[count]
					if self.debug:
						cprint("Error!", "red")
			except:
				del self.readPList[count]
				del self.respTimes[count]
				if self.debug:
					cprint("Bad Proxy: {}".format(proxy), "red")
			count += 1 
		count = 0
		for proxy in self.proxyList:
			if self.killed:
				break
			if len(self.readPList) > self.maxPoolSize:
				if self.debug:
					print("Exceded Max Pool Size, stopping Scraping...")
				break
			if self.debug:	
				cprint("Loading proxy # {}".format(count), "green")
			proxies = {
			  'http': proxy,
			  'https': proxy
			}
			try:
				r = requests.get("http://google.com", proxies=proxies, timeout=self.timeout)
				if(r.status_code == 200):
					responseTime = r.elapsed.total_seconds()

					inserted = False
					for x in range(0, len(self.readPList)):
						if self.respTimes[x] > responseTime:
							self.readPList.insert(proxy,x)
							self.respTimes.insert(responseTime,x)
					if not inserted:
						self.readPList.append(proxy)
						self.respTimes.append(responseTime)


					if self.debug:
						cprint("Working {0}! Reponse Time: {1}".format(proxy,responseTime),"green")
				else:
					if self.debug:
						cprint("Banned!", "red")
			except:
				if self.debug:
					cprint("Bad Proxy: {}".format(proxy), "red")
			count += 1


	def site1(self):
		url = "http://www.aliveproxy.com/fastest-proxies/"
		user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
		r = requests.get(url,headers=user)

		data = r.text
		soup = BeautifulSoup(data,"html.parser")
		for ips in soup.find_all("tr",{"class":"cw-list"}):
			for ip in ips.find_all("td",{"class":"dt-tb2"}):
				currIP = ip.renderContents().strip().decode('UTF-8')
				index = currIP.find('<')
				if(index != -1):
					if currIP[0:index] not in self.proxyList:
						self.proxyList.append(currIP[0:index])
				break;

	def site2(self):
		url = "https://www.us-proxy.org/"
		user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
		r = requests.get(url,headers=user)
		data = r.text
		soup = BeautifulSoup(data,"html.parser")

		table = soup.find("tbody")
		for ips in table.find_all("tr"):
			count = 0
			proxy = ""
			for ip in ips.find_all("td"):
				if count == 0:
					proxy = str(ip.text)
					proxy += ":"
				if count == 1:
					proxy += str(ip.text)
					if proxy not in self.proxyList:
						self.proxyList.append(proxy)
					break;
				count += 1

	def site3(self):
		url = "http://spys.ru/free-proxy-list/US/"
		user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
		
		r = requests.post(url,headers=user, data={"xpp":"1"})

		data = r.text
		soup = BeautifulSoup(data,"html.parser")

		proxy = ""
		regexProxy = "^.*(?=(document.write))"
		# for ips in soup.find_all("tr",{"class":"spy1xx"}):
		for ips in soup.find_all("tr"):
			count = 0
			for ip in ips.find_all("td",{"colspan":"1"}):
				# IP
				if count == 0:
					# rawProxy = str(ip.text)[2:20]
					proxy = str(re.sub('[a-z]','', str(ip.text)[2:20])).replace(" ","")
					if len(proxy) < 9:
						break;
				# Type:
				if count == 1:
					proxyType = str(ip.text)
					if "Squid" in proxyType:
						proxy += ":3128"
					elif "HTTPS" in proxyType:
						proxy += ":8080"
					elif "HTTP" in proxyType:
						proxy += ":80"
					elif "SOCKS5" in proxyType:
						proxy += ":1080"
					#new
					if proxy not in self.proxyList:
						self.proxyList.append(proxy)
					break;
				count += 1

	def site4(self):
		url = "https://www.proxynova.com/proxy-server-list/country-us/"
		user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
		
		r = requests.get(url,headers=user)
		data = r.text
		soup = BeautifulSoup(data,"html.parser")

		proxy = ""
		# for ips in soup.find_all("tr",{"class":"spy1xx"}):
		for ips in soup.find_all("tr"):
			count = 0
			for ip in ips.find_all("td",{"align":"left"}):
				if count == 0:
					proxy = str(ip.get_text(strip=True).replace("document.write('","").replace("'","").replace("+","").replace(");","").replace(" ",""))
				if count == 1:
					proxy += ":"+str(ip.text).strip()
					
					#1234567876.19.substr(8) LOL 
					currP = proxy.split('.substr(8)')
					formattedProxy = currP[0][8:] + currP[1]
					if formattedProxy not in self.proxyList:
						self.proxyList.append(formattedProxy)
					break;
				count += 1

	def kill(self):
		self.killed = True

