import Queue
import threading
import urllib2

# called by each thread
def get_url(q, url):
    if url == "http://bing.com":
        from trepan.api import debug;
        debug()
    q.put(urllib2.urlopen(url).read())

theurls = ["http://google.com",
           "http://yahoo.com",
           "https://github.com",
           "http://bing.com"]

q = Queue.Queue()

for u in theurls:
    t = threading.Thread(target=get_url, args = (q,u))
    # t.daemon = True
    t.start()

s = q.get()
print s
