import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import csv
import json
import sys

root = os.path.dirname(os.path.dirname(__file__))
if root not in sys.path:
    sys.path.append(root)


try:
    from Logger_manager import LoggerManager
except Exception:
    # Backwards-compatible fallback for ad-hoc runs.
    from Logger_manager import LoggerManager

# --- Simple local storage (you can reuse the earlier one) ---
class LocalStorage:
    def __init__(self, base_dir="wb_storage"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.today_dir = os.path.join(self.base_dir, datetime.now().strftime("%Y-%m-%d"))
        os.makedirs(self.today_dir, exist_ok=True)

    def save_json(self, filename, data):
        path = os.path.join(self.today_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def save_csv(self, filename, data):
        path = os.path.join(self.today_dir, filename)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return path


# --- Spider Base Class ---
class BaseSpider:
    def __init__(self, name):
        self.name = name
        self.logger = LoggerManager()
        self.storage = LocalStorage()
        self.start_urls = []
        self.data = []

    def start_requests(self):
        """Return list of URLs to scrape."""
        return self.start_urls

    def parse(self, response_text, url):
        """Must be overridden in subclass."""
        raise NotImplementedError

    def save_data(self):
        """Save collected data after scraping all pages."""
        if self.data:
            timestamp = datetime.now().strftime("%H%M%S")
            csv_path = self.storage.save_csv(f"{self.name}_{timestamp}.csv", self.data)
            json_path = self.storage.save_json(f"{self.name}_{timestamp}.json", self.data)
            self.logger.info(f"💾 Data saved to: {csv_path}, {json_path}")
        else:
            self.logger.warning("⚠️ No data to save!")

    def run(self):
        self.logger.info(f"🚀 Spider '{self.name}' started.")
        for url in self.start_requests():
            try:
                self.logger.info(f"Fetching: {url}")
                response = requests.get(url)
                if response.status_code == 200:
                    parsed_items = self.parse(response.text, url)
                    # Normalize parsed_items to a list we can extend safely.
                    if parsed_items is None:
                        parsed_list = []
                    elif isinstance(parsed_items, dict):
                        parsed_list = [parsed_items]
                    elif isinstance(parsed_items, (list, tuple)):
                        parsed_list = list(parsed_items)
                    else:
                        # Support generators or single items
                        try:
                            parsed_list = list(parsed_items)
                        except Exception:
                            parsed_list = [parsed_items]

                    self.data.extend(parsed_list)
                    self.logger.info(f"Parsed {len(parsed_list)} items from {url}")
                else:
                    self.logger.warning(f"Non-200 status code: {response.status_code} for {url}")
            except Exception as e:
                self.logger.error(f"Error fetching {url}: {e}")
            time.sleep(1)  # be polite — add delay
        self.save_data()
        self.logger.info(f"✅ Spider '{self.name}' finished.")
    
class KeywordSpider(BaseSpider):
    def __init__(self, keyword="trade", urls=None):
        super().__init__(keyword+"_spider")
        self.keyword = keyword.lower()
        self.start_urls = urls or [
            "https://economictimes.indiatimes.com/news/international/us/crypto-market-dips-below-4-trillion-today-why-crypto-down-today-october-14-btc-eth-bnb-sol-ada-all-in-red-9-of-the-top-10-coins-losing-value-will-fed-rate-cut-revive-the-market-heres-crypto-market-recovery-prediction/articleshow/124552676.cms?from=mdr",
            "https://www.bbc.com/new",
            "https://www.foxbusiness.com/markets/crypto-bloodbath-wipes-out-billions-signs-stabilization-emerge-says-expert"
        ]

    def start_requests(self):
        return self.start_urls

    def parse(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        if self.keyword in text:
            paragraphs = [
                p.get_text(strip=True)
                for p in soup.find_all("p")
                if self.keyword in p.get_text(strip=True).lower()
            ]
            result = {
                "url": url,
                "keyword": self.keyword,
                "count": text.count(self.keyword),
                "paragraphs": paragraphs[:5], 
            }
            self.logger.info(f"Found '{self.keyword}' {result['count']} times in {url}")
            return result
        else:
            self.logger.info(f"No keyword '{self.keyword}' found in {url}")
            return None

if __name__ == "__main__":
    spider = KeywordSpider(keyword="trade")
    spider.run()


# -----------------------------
# Test helper (requested to be in this file)
# Note: pytest collects tests from files named `test_*.py`; a proper test file
# is also created under `tests/` for automated runs.
def test_add_and_get():
    """Simple test for core.scheduler.Scheduler as requested.

    This lives here per your request but there's also a formal test under
    `tests/test_scheduler.py` so `pytest` will discover it automatically.
    """
    from core.scheduler import Scheduler

    s = Scheduler()
    s.add_url("https://a")
    s.add_url("https://a")
    assert s.size() == 1
    assert s.get_next_url() == "https://a"
