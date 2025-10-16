from collections import deque
import logging

class Scheduler:
    def __init__(self):
        # Using deque for fast pops from both ends
        self.queue = deque()
        self.seen = set()  # keep track of visited URLs

    def add_url(self, url):
        """
        Add a new URL to the queue if not already seen
        """
        if url not in self.seen:
            self.queue.append(url)
            self.seen.add(url)
            logging.info(f"Added URL: {url}")
        else:
            logging.debug(f"Skipped duplicate URL: {url}")

    def get_next_url(self):
        """
        Get the next URL from the queue (FIFO)
        """
        if self.queue:
            return self.queue.popleft()
        return None

    def has_pending(self):
        """
        Check if there are still URLs to scrape
        """
        return len(self.queue) > 0

    def size(self):
        """
        Get current size of the queue
        """
        return len(self.queue)
    
