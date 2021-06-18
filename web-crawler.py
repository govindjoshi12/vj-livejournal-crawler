from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin, urlparse
from urllib.error import HTTPError
from http.client import InvalidURL
from ssl import _create_unverified_context

class AnchorParser(HTMLParser):
    def __init__(self, baseURL = ""):
        HTMLParser.__init__(self)
        
        # All hyperlinks in a webpage
        self.pageLinks = set()
        self.baseURL = baseURL
    
    def getLinks(self):
        return self.pageLinks
    
    # attrs: All attributes inside tag. (Ex. id, target, etc.)
    # Overriding super class method
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for (attrib, value) in attrs:
                if attrib == "href":
                    # accounts for absolute or relative path
                    absUrl = urljoin(self.baseURL, value)

                    # Make sure url is valid (http/https)
                    if urlparse(absUrl).scheme in ["http", "https"]:
                        self.pageLinks.add(absUrl)

class MyWebCrawler(object):
    def __init__(self, url, maxCrawl=10):
        self.visited = set()
        self.starterURL = url
        self.max = maxCrawl
    
    def getVisited(self):
        return self.visited
    
    def parse(self, url):
        # ignore certificate validation
        try:
            htmlContent = urlopen(url, context=_create_unverified_context()).read().decode()
            parser = AnchorParser(url)
            parser.feed(htmlContent)
            return parser.getLinks()
        except(HTTPError, InvalidURL, UnicodeDecodeError):
            print("FAILED: {}".format(url))
            return set() #Empty set

    def crawl(self):
        urlsToParse = {self.starterURL}
        while(len(urlsToParse) > 0 and len(self.visited < self.max)):
            nextUrl = urlsToParse.pop()
            if nextUrl not in self.visited:
                print("Parsing: {}".format(nextUrl))
                urlsToParse |= self.parse(nextUrl)
                self.visited.add(nextUrl)

if __name__ == "__main__":
    