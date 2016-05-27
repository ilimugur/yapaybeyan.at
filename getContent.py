import urllib2
from BeautifulSoup import BeautifulSoup, NavigableString
import re

def getDomainURL(url):
    slashToLookFor = 1
    if url.find("http://") > -1 or url.find("https://") > -1:
        slashToLookFor = 3
    endIndex = 0
    for i in range(0, slashToLookFor):
        endIndex = url.find("/", endIndex) + 1
    return url[:endIndex]

def get(url, listLocation, unitLocation, isLink = False, stripTagsInUnit = False):
    '''
    Search url and retrieve a desired list of links or content.

    Keyword arguments:
        listLocation -- list of dictionaries to specifically locate container of content
        unitLocation -- list of dictionaries to specifically locate a unit of content in container
        isLink -- boolean value indicating what is sought: href or content (default False)

    Return value:
        List of contents or URLs, based on the value of isLink argument.

    Notes:
        - Lists listLocation and unitLocation should only contain dictionaries.
        - Each dict must have a value assigned for exactly 1 of the keys "id", "style", "class" or "tag".
        - While parsing HTML, those keys are checked in a specific-to-general order for each dict.
        - "id" is checked first, followed by "style", "class" and "tag", respectively.
    '''
    pageHTML = urllib2.urlopen(url)
    soup = BeautifulSoup(pageHTML)

    for container in listLocation:
        if container.has_key("id"):
            soup = soup.find(id = container["id"])
        elif container.has_key("style"):
            soup = soup.find(style = container["style"])
        elif container.has_key("tag"):
            classDict = {}
            if container.has_key("class"):
                classDict["class"] = container["class"]
            soup = soup.find(container["tag"], classDict)
        else:
            print "Error!"

    result = []
    domainURL = getDomainURL(url)

    soup = [soup]
    for container in unitLocation:
        new_soup = []
        if container.has_key("id"):
            for s in soup:
                new_soup += s.findAll(id = container["id"])
        elif container.has_key("style"):
            for s in soup:
                new_soup += s.findAll(style = container["style"])
        elif container.has_key("tag"):
            classDict = {}
            if container.has_key("class"):
                classDict["class"] = container["class"]
            for s in soup:
                new_soup += s.findAll(container["tag"], classDict)
        else:
            print "Error!"
        soup = new_soup

    for listElement in soup:
        if isLink:
            link = listElement.get("href")
            if link.find("http://") == -1 and link.find("https://") == -1:
                link = domainURL + link
            resultUnit = link
        else:
            resultUnit = u""

            for content in listElement.contents:
                if type(content) is NavigableString or not stripTagsInUnit:
                    resultUnit += unicode(content)
                else:
                    resultUnit += re.sub("<.*?>", "", unicode(content))
        result.append(resultUnit)

    return result
