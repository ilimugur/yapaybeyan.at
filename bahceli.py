from getContent import *

def getSpeechLinks():
    result = []
    for i in range(1999, 2017):
        url = "http://88.255.31.62/htmldocs/genel_baskan/1553/konusmalari/Devlet_Bahceli_" + str(i) + "_yili_konusmalari.html"
        listLocation = [{'id':'mhpmaincontent'}, {'tag':'td', 'class':'ana_icerik'}, {'tag':'table'}]
        unitLocation = [{'tag':'tr'}, {'tag':'a', 'class':'mhp_table_link'}]
        result += get(url, listLocation, unitLocation, True)
        print "Got from: " + url
    return result

def getSpeech(url):
    result = []
    listLocation = [{'tag':'td', 'class':'ana_icerik'}]
    unitLocation = [{'tag':'p', 'class':'govdeverdana'}]

    paragraphList = get(url, listLocation, unitLocation, False, True)

    result = "\n".join(paragraphList) + "\n"

    return result

if __name__ == "__main__":
    f = open('Bahceli.txt', 'w')
    speechLinks = getSpeechLinks()
    remainingSpeechs = len(speechLinks)
    for speechLink in speechLinks:
        f.write((getSpeech(speechLink) + "\n").encode('utf8'))
        print "Remaining: " + str(remainingSpeechs)
        remainingSpeechs -= 1
    f.close()
