from scheduler import Scheduler

scheduler = Scheduler()

# Add some URLs
scheduler.add_url("https://x.com/home")
scheduler.add_url("https://www.instagram.com/explore/")
scheduler.add_url("https://x.com/home")  # duplicate (ignored)

print("Queue size:", scheduler.size())

# Process URLs
while scheduler.has_pending():
    url = scheduler.get_next_url()
    print("Scraping:", url)
