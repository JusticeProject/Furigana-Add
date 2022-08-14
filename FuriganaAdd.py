import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import time
import random

###################################################################################################

CUSTOM_HTTP_HEADER = {
    "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"en-US,en;q=0.9",
    "Referer":"https://www.google.com/"
}

###################################################################################################

def get_html(url):
    for i in range(0, 5):
        try:
            result = requests.get(url, headers=CUSTOM_HTTP_HEADER, timeout=5)
            return result.text
        except BaseException as e:
            strError = str(e.args)
            print("failed to retrieve html: " + strError)
            time.sleep(i + 5)

    return ""

###################################################################################################

def get_furigana(kanji):
    base_url = "https://jisho.org/search/"
    url_parsed = base_url + quote(kanji)
    html = get_html(url_parsed)
    bs = BeautifulSoup(html, "html.parser")

    # get the furigana for the first result
    span = bs.find("span", {"class": "furigana"})
    if (span is None):
        print("could not find " + kanji)
        return []
    
    spans = span.find_all("span")
    hiragana_list = []
    for item in spans:
        if len(item.text) > 0:
            hiragana_list.append(item.text)
    print("found " + str(hiragana_list) + " for " + kanji)
    return hiragana_list

###################################################################################################

words = open("words.txt", "r", encoding="utf-8").readlines()
passage = open("passage.txt", "r", encoding="utf-8").read()

# remove duplicates
words = [word.strip() for word in words]
words = list(set(words))
print(f"length of word list = {len(words)}")

for line in words:
    line_split = line.split(",")
    compound_word = line_split[0]
    separate_kanji = line_split[1:]
    furigana_list = get_furigana(compound_word)
    
    if (len(separate_kanji) == 0):
        print("combining the furigana")
        furigana = "".join(furigana_list)
        ruby = "<ruby>" + compound_word + "<rt>" + furigana + "</rt></ruby>"
        passage = passage.replace(compound_word, ruby)
    elif (len(separate_kanji) != len(furigana_list)):
        print("not sure what to do with the furigana")
        ruby = "<ruby>" + compound_word + "<rt></rt></ruby>"
        passage = passage.replace(compound_word, ruby)
    else:
        print("matching kanji with its furigana")
        ruby = compound_word
        kanji_furigana = list(zip(separate_kanji, furigana_list))
        for kanji,furigana in kanji_furigana:
            ruby = ruby.replace(kanji, "<ruby>" + kanji + "<rt>" + furigana + "</rt></ruby>")
        passage = passage.replace(compound_word, ruby)
    
    time.sleep(random.randint(30, 90))

passage = passage.replace("\n", "<br>\n")
output = open("updated_passage.txt", "w", encoding="utf-8")
output.write(passage)
output.close()
print("done!")
