from getContent import *
import sys
import re

def getSpeechLinks():
    result = []
    urls = ["http://chp.org.tr/Konusmalar/38/EtkinlikKonusmalari.aspx",
            "http://chp.org.tr/Konusmalar/36/TBMMGrupKonusmalari.aspx",
            "http://chp.org.tr/Konusmalar/37/Miting.aspx",
]
    for url in urls:
        listLocation = [{'tag':'div', 'class':'chp-content-text'}, {'tag':'table'}]
        unitLocation = [{'tag':'td'}, {'tag':'a'}]
        result += get(url, listLocation, unitLocation, True)
        print "Got from: " + url
    return result

def getSpeech(url):
    result = []
    listLocation = [{'tag':'div', 'class':'chp-left-box chp-news'}]
    unitLocation = [{'tag':'div', 'class':'chp-content-text'}]

    paragraphList = get(url, listLocation, unitLocation, False)

    result = u"\n".join(paragraphList) + u"\n"
    result = re.sub(r"<.?span[^>]*>|<.?h[1-5][^>]*>|<.?em[^>]*>|<.?p[^>]*>|<br[^>]*>|<img[^>]+>", "", result)
    result = re.sub(r"<iframe[^>]+><.iframe>", "", result)
    result = re.sub(r"<strong>[^>]+<.strong>", "", result)

    return result

if __name__ == "__main__":
    f = open('Kilicdaroglu.txt', 'w')
    speechLinks = getSpeechLinks()
    remainingSpeechs = len(speechLinks)
    for speechLink in speechLinks:
        try:
            f.write((getSpeech(speechLink) + u"\n").encode('utf8'))
        except UnicodeEncodeError:
            print "Error:", sys.exc_info()[0]
        print "Remaining: " + str(remainingSpeechs)
        remainingSpeechs -= 1
    f.close()
