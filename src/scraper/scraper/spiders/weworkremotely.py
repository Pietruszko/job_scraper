import scrapy

class WeWorkRemotelySpider(scrapy.Spider):
    name = "weworkremotely"
    allowed_domains = ["weworkremotely.com"]
    start_urls = ["https://weworkremotely.com/categories/remote-programming-jobs"]

    def parse(self, response):
        """Extract job listing links from the main page"""
        job_links = response.css("section.jobs article ul li a::attr(href)").getall()
        for job in job_links:
            job_url = response.urljoin(job)
            if "/remote-jobs/" in job_url:  # ✅ Ensure it's a job listing
                self.logger.info(f"🔗 Found Job URL: {job_url}")  
                yield scrapy.Request(job_url, callback=self.parse_job)


    def parse_job(self, response):
        """Extract job details from individual job pages"""
        yield {
            "title": response.css("h2.lis-container__header__hero__company-info__title::text").get(),
            "company": response.css("div.lis-container__job__sidebar__companyDetails h3::text").get(),
            "salary": response.css("div.lis-container__job__sidebar__job-about ul li:nth-child(4) a span::text").get(),
            "region": response.css("div.lis-container__job__sidebar__job-about ul li:nth-child(6) div::text").get(),
            "description": response.css("div.lis-container__job__content__description::text").get(),
            "url": response.url,
        }

