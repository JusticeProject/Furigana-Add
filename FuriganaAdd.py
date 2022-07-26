from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import time
import random

###################################################################################################

def get_furigana(kanji):
    base_url = "https://jisho.org/search/"
    url_parsed = base_url + quote(kanji)
    html = urlopen(url_parsed)
    bs = BeautifulSoup(html, "html.parser")

    # get the furigana for the first result
    span = bs.find("span", {"class": "furigana"})
    if (span is None):
        return ""
    
    spans = span.find_all("span")
    hiragana_list = [item.text for item in spans]
    hiragana = "".join(hiragana_list)
    print("found " + hiragana + " for " + kanji)
    return hiragana

###################################################################################################

words = open("words.txt", "r", encoding="utf-8").readlines()
passage = open("passage.txt", "r", encoding="utf-8").read()

for kanji in words:
    add_breaks = False
    if ("\n" in kanji):
        add_breaks = True
        
    kanji = kanji.strip()
    furigana = get_furigana(kanji)
    ruby = "<ruby>" + kanji + "<rt>" + furigana + "</rt></ruby>"

    if (add_breaks):
        ruby += "<br>"
    
    passage = passage.replace(kanji, ruby)
    time.sleep(random.randint(30, 90))

output = open("updated_passage.txt", "w", encoding="utf-8")
output.write(passage)
output.close()
print("done!")
