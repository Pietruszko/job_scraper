import psycopg2
from scrapy.exceptions import DropItem
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class PostgreSQLPipeline:
    def __init__(self):
        # Connect to PostgreSQL
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        """Save job listing to PostgreSQL"""
        try:
            self.cursor.execute("""
                INSERT INTO jobs_job (title, company, salary, region, description, url, posted_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)  
                ON CONFLICT (url) DO NOTHING;
            """, (item["title"], item["company"], item["salary"], item["region"], item["description"], item["url"], item["posted_date"]))
        
            self.conn.commit()
            return item
        except Exception as e:
            spider.logger.error(f"Database Error: {e}")
            raise DropItem(f"Error inserting item: {e}")


    def close_spider(self, spider):
        """Close database connection when Scrapy finishes"""
        self.cursor.close()
        self.conn.close()
