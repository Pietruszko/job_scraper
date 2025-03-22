import os
import sys
import django
from django.db import connection
import datetime
import re
import scrapy

# Set up Django in Scrapy
#sys.path.append(os.path.join(os.path.dirname(__file__), "../../../api"))  # Adjust the path to your Django project if needed
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")  # Update this to match your project
#django.setup()
#from jobs.models import Job  # Now Django models will work

def parse_relative_date(text):
    """Convert 'Posted X days ago' into an actual date (YYYY-MM-DD)."""
    match = re.search(r'(\d+) days? ago', text)
    if match:
        days_ago = int(match.group(1))
        return (datetime.date.today() - datetime.timedelta(days=days_ago)).isoformat()
    return None

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
        salary = response.css("li:has(a[href*='-salary-jobs']) span.box::text").get()
        description = " ".join(response.css("div.lis-container__job__content__description *::text").getall()).strip()
        region = response.css("li:has(a[href*='-remote-jobs']) span.box::text").get()
        
        posted_date_raw = response.css("p.lis-container__header__hero__company-info__icons__item span::text").get()
        posted_date = parse_relative_date(posted_date_raw)

        yield {
            "title": response.css("h2.lis-container__header__hero__company-info__title::text").get(),
            "company": response.css("div.lis-container__job__sidebar__companyDetails h3::text").get(),
            "salary": salary,
            "region": region,
            "description": description,
            "posted_date": posted_date,
            "url": response.url,
        }
