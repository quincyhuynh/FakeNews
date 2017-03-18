from aylienapiclient import textapi
import re
from urlparse import urlparse

client = textapi.Client("4657dfa6", "bbfd5faa23a1020d92e946dd83bce6b7")

urls = ["http://techcrunch.com/2015/04/06/john-oliver-just-changed-the-surveillance-reform-debate", "http://www.businessinsider.com/trump-ballistic-over-sessions-recusal-russia-ties-in-meeting-2017-3", "https://www.yahoo.com/news/jordan-executes-10-men-convicted-terror-charges-070601468.html"]

for url in urls:
	extract = client.Extract({"url": url, "best_image": False})

	print "\nURL: " + url
	print "Company domain: " + re.sub('www.', '', urlparse(url).hostname)
	print "Title: " + extract['title']
	print "Author: " + extract['author']
	print "Date published: " + extract['publishDate']
	print "Article: " + extract['article']