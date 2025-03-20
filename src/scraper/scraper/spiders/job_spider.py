import scrapy
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.http import HtmlResponse

class JobSpider(scrapy.Spider):
    name = "job_spider"
    allowed_domains = ["remoteok.com"]
    start_urls = ["https://remoteok.com/remote-jobs"]

    def start_requests(self):
        # Setup Selenium with ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(self.start_urls[0])  # Open RemoteOK job page

        time.sleep(3)  # Wait for Cloudflare check to complete

        # Get page source and pass it to Scrapy
        scrapy_response = HtmlResponse(url=self.start_urls[0], body=driver.page_source, encoding="utf-8")
        driver.quit()  # Close Selenium browser

        yield from self.parse(scrapy_response)  # Send to Scrapy parser

    def parse(self, response):
        self.logger.info(f"Accessing page: {response.url}")
        for job in response.css("tr.job"):
            job_url = response.urljoin(job.css("a[itemprop='url']::attr(href)").get())
            self.logger.info(f"Found job URL: {job_url}")
            yield response.follow(job_url, callback=self.parse_job)

    def parse_job(self, response):
        yield {
            "title": response.css("h2[itemprop='title']::text").get(),
            "company": response.css("h3[itemprop='name']::text").get(),
            "location": response.css("div.location::text").get(),
            "description": response.css("div.markdown::text").get(),
            "url": response.url,
        }
