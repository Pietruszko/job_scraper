BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

# Use a real browser User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Stop after scraping 10 jobs
CLOSESPIDER_ITEMCOUNT = 10

# Remove unnecessary middleware (since Selenium is used)
# DOWNLOADER_MIDDLEWARES = {}

# No need for AutoThrottle
AUTOTHROTTLE_ENABLED = False

# No need for DOWNLOAD_DELAY (Selenium handles waiting)
DOWNLOAD_DELAY = 0



# Enable cookies if needed
# COOKIES_ENABLED = True

# Keep real browser headers (optional)
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://weworkremotely.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

ITEM_PIPELINES = {
    "scraper.pipelines.PostgreSQLPipeline": 300,  # Activate pipeline
}


# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
