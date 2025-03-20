import scrapy

class JobSpider(scrapy.spiders.SitemapSpider):
    name = "job_spider"
    allowed_domains = ["remoteok.com"]

    # RemoteOK's main sitemap file
    sitemap_urls = ["https://remoteok.com/sitemap.xml"]

    # Extract only job listing pages
    sitemap_rules = [
        (r"/remote-jobs/", "parse_job"),
    ]

    def parse(self, response):
        for job in response.css("tr.job"):  # Select job listings
            job_url = response.urljoin(job.css("a[itemprop='url']::attr(href)").get())  # Get job URL
            
            yield response.follow(job_url, callback=self.parse_job)  # Follow job link to scrape full details


    def parse_job(self, response):
        yield {
            "title": response.css("h2[itemprop='title']::text").get(),
            "company": response.css("h3[itemprop='name']::text").get(),
            "location": response.css("div.location::text").get(),
            "description": response.css("div.markdown::text").get(),
            "url": response.url,
        }

