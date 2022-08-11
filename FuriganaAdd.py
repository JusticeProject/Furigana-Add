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
