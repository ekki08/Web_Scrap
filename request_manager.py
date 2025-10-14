import requests
import time
import random
import logging

class RequestManager:
    def __init__(self, headers=None, proxies=None, max_retries=3, delay_range=(1, 3)):
        """
        :param headers: dict, default headers for requests
        :param proxies: list, optional proxy list
        :param max_retries: int, number of retry attempts
        :param delay_range: tuple, (min, max) seconds for random delay
        """
        self.session = requests.Session()
        self.headers = headers or {"User-Agent": "MyScraperBot/1.0"}
        self.proxies = proxies or []
        self.max_retries = max_retries
        self.delay_range = delay_range

    def get(self, url, params=None):
        """
        Perform GET request with retries, delay, headers, and proxy rotation
        """
        for attempt in range(self.max_retries):
            try:
                # Add delay to be polite
                delay = random.uniform(*self.delay_range)
                time.sleep(delay)

                # Rotate proxy if available
                proxy = random.choice(self.proxies) if self.proxies else None
                proxy_dict = {"http": proxy, "https": proxy} if proxy else None

                response = self.session.get(
                    url,
                    headers=self.headers,
                    proxies=proxy_dict,
                    params=params,
                    timeout=10
                )
                response.raise_for_status()  # raise error if 4xx or 5xx
                return response

            except requests.RequestException as e:
                logging.warning(f"Attempt {attempt+1} failed for {url}: {e}")
                if attempt == self.max_retries - 1:
                    logging.error(f"Giving up on {url}")
                    return None

    def post(self, url, data=None, json=None):
        """
        Perform POST request (similar to get)
        """
        try:
            response = self.session.post(
                url,
                headers=self.headers,
                data=data,
                json=json,
                timeout=10
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"POST request failed for {url}: {e}")
            return None
