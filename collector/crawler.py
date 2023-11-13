from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, TimeoutException
from bs4 import BeautifulSoup
from bs4.element import Comment

from urllib.parse import quote_plus, urlparse
import abc
import time


class Crawler:
	def __init__(self):
		self.driver = Driver()
		self.google = Google(self.driver.get())
		self.naver = Naver(self.driver.get())
		self.page_crawler = PageCrawler(self.driver.get())

	def start(self, keyword) -> list:
		data = []
		data += self.google.start(keyword)
		data += self.naver.start(keyword)
		
		for d in data:
			content = self.page_crawler.start(d["url"])
			d["content"] = content
			time.sleep(3)

		self.driver.close()
		
		return data


class Driver:
	def __init__(self):
		self.options = webdriver.ChromeOptions()
		self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
		# self.options.add_argument("headless")
		# self.options.add_argument("window-size=1920x1080")
		# self.options.add_argument("disable-gpu")
		self.driver = webdriver.Chrome(options=self.options)
		self.driver.set_page_load_timeout(10)
		
	def get(self):
		return self.driver

	def close(self):
		self.driver.close()


class EngineCrawler(abc.ABC):
	def __init__(self, driver):
		self.driver = driver
		self.site = ""

	def get_source(self, keyword):
		url = self.site + quote_plus(keyword)
		
		self.driver.get(url=url)
		source = self.driver.page_source

		return source

	@abc.abstractmethod
	def crawl_weblist(self, source) -> list:
		pass

	def filter_page_to_pass(self, url):
		blacklist = [
			"www.wordreference.com",
			"dictionary.cambridge.org",
			"www.dictionary.com"
		]

		if urlparse(url).netloc in blacklist:
			return True
		return False


class Google(EngineCrawler):
	def __init__(self, driver):
		super(Google, self).__init__(driver)
		self.site = "https://www.google.com/search?q="

	def start(self, keyword):
		source = self.get_source(keyword)
		data = self.crawl_weblist(source)

		return data
	
	def crawl_weblist(self, source):
		data = []
		
		soup = BeautifulSoup(source, "html.parser")
		data += self.crawl_total(soup)

		return data

	def crawl_total(self, soup):
		data = []
		
		items = soup.select("div.MjjYud>div>div.N54PNb.BToiNc.cvP2Ce")
		for item in items:
			title = item.select_one("span>a>h3").text
			url = item.select_one("span>a")["href"]

			if self.filter_page_to_pass(url):
				continue

			preview = item.find(attrs={"data-sncf":"1"}).select("span")
			if len(preview) > 1:
				preview = preview[-1].text
			elif len(preview) < 1:
				preview = ""
			else:
				preview = preview[0].text

			data.append({
				"title": title,
				"url": url,
				"preview": preview
			})
		
		return data


class Naver(EngineCrawler):
	def __init__(self, driver):
		super(Naver, self).__init__(driver)
		self.site = "https://search.naver.com/search.naver?query="

	def start(self, keyword):
		source = self.get_source(keyword)
		data = self.crawl_weblist(source)

		return data

	def crawl_weblist(self, source):
		data = []

		soup = BeautifulSoup(source, "html.parser")
		data += self.crawl_total(soup)
		data += self.crawl_view(soup)
		data += self.crawl_news(soup)
		data += self.crawl_kin(soup)

		return data

	def crawl_total(self, soup):
		data = []
		
		items = soup.select("section>div>ul.lst_total>li.bx")
		for item in items:
			try:
				title = item.select_one("div.total_group>div.total_tit>a").text
				url = item.select_one("div.total_group>div.total_tit>a")["href"]
				if self.filter_page_to_pass(url):
					continue

				preview = item.select_one("div.total_group>div.total_dsc_wrap>a")
				if not preview:
					preview = ""
				else:
					preview = preview.text
			except AttributeError:
				continue

			data.append({
				"title": title,
				"url": url,
				"preview": preview
			})
			
		return data

	def crawl_view(self, soup):
		data = []

		items = soup.select("section>div>ul.lst_view>li.bx")
		for item in items:
			try:
				title = item.select_one("div.title_area>a").text
				url = item.select_one("div.title_area>a")["href"]
				if self.filter_page_to_pass(url):
					continue

				preview = item.select_one("div.dsc_area>a")
				if not preview:
					preview = ""
				else:
					preview = preview.text
			except AttributeError:
				continue

			data.append({
				"title": title,
				"url": url,
				"preview": preview
			})

		return data

	def crawl_news(self, soup):
		data = []

		items = soup.select("section>div>div.group_news>ul.list_news>li.bx")
		for item in items:
			try:
				title = item.select_one("div.news_contents>a.news_tit").text
				url = item.select_one("div.news_contents>a.news_tit")["href"]
				if self.filter_page_to_pass(url):
					continue

				preview = item.select_one("div.news_contents>div.news_dsc>div>a")
				if not preview:
					preview = ""
				else:
					preview = preview.text
			except AttributeError:
				continue

			data.append({
				"title": title,
				"url": url,
				"preview": preview
			})
			
		return data

	def crawl_kin(self, soup):
		data = []

		items = soup.select("section>div>ul.lst_nkin>li.bx")
		for item in items:
			try:
				title = item.select_one("div.question_group>a").text
				url = item.select_one("div.question_group>a")["href"]
				if self.filter_page_to_pass(url):
					continue

				preview = item.select_one("div.answer_group>a")
				if not preview:
					preview = ""
				else:
					preview = preview.text
			except AttributeError:
				continue

			data.append({
				"title": title,
				"url": url,
				"preview": preview
			})
			
		return data


class PageCrawler:
	def __init__(self, driver):
		self.driver = driver

	def start(self, url):
		try:
			headers = {""}
			self.driver.get(url=url)
		except InvalidArgumentException:
			text = ""
		except TimeoutException:
			text = ""
		finally:
			source = self.driver.page_source
			text = self.text_from_html(source)
			print()

		return text

	def text_from_html(self, source):
		soup = BeautifulSoup(source, 'html.parser')
		texts = soup.findAll(string=True)
		visible_texts = filter(self.tag_visible, texts)

		return u" ".join(t.strip() for t in visible_texts)

	def tag_visible(self, element):
		if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
			return False
		if isinstance(element, Comment):
			return False
		return True

