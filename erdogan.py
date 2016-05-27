from getContent import *

def getSpeechLinks():
    result = []
    for i in range(1, 7):
        url = "http://tccb.gov.tr/kategori/353/kategori/" + str(i) + ".html"
        listLocation = [{'id':'right-column'}, {'id':'sub-page-wrapper'}, {'id':'list-press-address'}, {'id':'divContentList'}]
        unitLocation = [{'tag':'dl'}, {'tag':'dd'}, {'tag':'a'}]
        result += get(url, listLocation, unitLocation, True, False)
        print "Got from: " + url
    return result

def getSpeech(url):
    result = []
    listLocation = [{'id':'right-column'}, {'id':'news-detail'}, {'id':'news-detail-body'}, {'id':'divContentArea'}]
    unitLocation = [{'tag':'p'}]

    speechList = get(url, listLocation, unitLocation, False, False)
    result = '\n'.join(speechList)
    return result

if __name__ == "__main__":
    f = open('Erdogan.txt', 'w')
    speechLinks = getSpeechLinks()
    remainingSpeeches = len(speechLinks)
    for speechLink in speechLinks:
        f.write((getSpeech(speechLink) + "\n\n").encode('utf8'))
        print "Remaining: " + str(remainingSpeeches)
        remainingSpeeches -= 1
    f.close()
