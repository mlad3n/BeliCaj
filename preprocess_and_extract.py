import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
import sklearn
from sklearn.feature_extraction import DictVectorizer
import random

body1 = """
Now you have chance to buy builder and panel of one of the best Banking Trojan on the Market.

Standard Version Features:
1.) Web injector and logger of browsers.
2.) grab: ftp accounts pop3 accounts
3.) autosave passwords and froms from browsers cookies
4.) flash
5.) certificate
6.) socks
7.) screenshots
8.) vnc module ( if paid )

Hide VNC module compatible with:
1.Windows XP x32, x64
2.Windows Vista x32, x64
3.Windows 7 x32, x64
4.Windows 8 x32, x64
5.Windows 8.1 x32, x64
6.Windows 10 x32, x64
7.Windows server

Browsers:
.) Internet explorer 8-11
.) Firefox All Version
.) Chrome

Panda will be supported and has updates.
Standard 7500 usd
Standard+VNC 15000 usd, 3 month free updates.
Trial deposit 1000 usd

Are you interested in buying?
slayed@exploit.im
"""

title1 = "**** Panda Banking Trojan ****"
body2 = """
Works for :

Win xp,vista office 7,10
Win7 office 7,10,13
Win 8 office 7,1o
win 8.1 office 7,10
Win 10 office 7,10

Main JID : slayed@exploit.im
Backup JID : slayed@creep.im / slayed@dvo.ru
"""
title2 = "MS Word CVE-2016-7193"

sites = [[body1, title1, "Botnets & Malware", "Slayed", 7500, ["panda bot", "panda botnet"]], [body2, title2, "exploits", "slayed", 3500, ["ms word", "microsoft exploit"]]]

tokenizer = RegexpTokenizer(r'\w+')
stop = set(stopwords.words('english'))
n = 3
feature_list1 = []
feature_list2 = []

for site in sites:

    body = site[0]
    title = site[1]
    group = site[2]
    vendor = site[3]
    price = site[4]
    tags = site[5]

    # TOKENIZE AND LOWERCASE
    body_lower_tokenized = tokenizer.tokenize(body.lower())
    title_lower_tokenized = tokenizer.tokenize(title.lower())

    # STOPWORDS REMOVAL
    body_stop_lower_tokenized = [word for word in body_lower_tokenized if word not in stop]
    title_stop_lower_tokenized = [word for word in title_lower_tokenized if word not in stop]

    # (RANDOM SPLIT IN TWO HALVES)
    body_shuffled = random.shuffle(body_stop_lower_tokenized)
    body_1 = body_shuffled[:(round(len(body_stop_lower_tokenized) / 2), 1)]
    body_2 = body_shuffled[round((len(body_stop_lower_tokenized) / 2), 1) + 1:]

    title_shuffled = random.shuffle(title_stop_lower_tokenized)
    title_1 = body_shuffled[:(len(title_stop_lower_tokenized) / 2)]
    title_2 = body_shuffled[(len(title_stop_lower_tokenized) / 2) + 1:]

    # EXTRACT 3GRAMS (FOR EACH HALF SEPARATELY)
    body_1_trigrams_init = [[word[i:i+n] for i in range(len(word)-n+1)] for word in body_1]
    body_1_trigrams = [trigram for trigram_list in body_1_trigrams_init for trigram in trigram_list]
    title_1_trigrams_init = [[word[i:i+n] for i in range(len(word)-n+1)] for word in title_1]
    title_1_trigrams = [trigram for trigram_list in title_1_trigrams_init for trigram in trigram_list]

    body_2_trigrams_init = [[word[i:i+n] for i in range(len(word)-n+1)] for word in body_2]
    body_2_trigrams = [trigram for trigram_list in body_2_trigrams_init for trigram in trigram_list]
    title_2_trigrams_init = [[word[i:i+n] for i in range(len(word)-n+1)] for word in title_2]
    title_2_trigrams = [trigram for trigram_list in title_2_trigrams_init for trigram in trigram_list]

    # MARK TITLE
    title_1_marked = ['t_' + word for word in title_1]
    title_1_trigrams_marked = ['t_' + trigram for trigram in title_1_trigrams]

    title_2_marked = ['t_' + word for word in title_1]
    title_2_trigrams_marked = ['t_' + trigram for trigram in title_2_trigrams]

    # COUNT THAT SHIT
    body_1_word_counter = Counter(body_1)
    body_1_trigram_counter = Counter(body_1_trigrams)
    title_1_word_counter = Counter(title_1_marked)
    title_1_trigram_counter = Counter(title_1_trigrams_marked)

    body_2_word_counter = Counter(body_2)
    body_2_trigram_counter = Counter(body_2_trigrams)
    title_2_word_counter = Counter(title_2_marked)
    title_2_trigram_counter = Counter(title_2_trigrams_marked)

    text_features_1 = body_1_word_counter + body_1_trigram_counter + title_1_word_counter + title_1_trigram_counter
    text_features_1 += Counter({'ve_' + vendor: 1}) + \
        Counter({'gr_' + group: 1}) + \
        Counter({'pr_price': price}) + \
        Counter(['tag_' + tag for tag in tags])
    text_features_2 = body_2_word_counter + body_2_trigram_counter + title_2_word_counter + title_2_trigram_counter
    text_features_2 += Counter({'ve_' + vendor: 1}) + \
        Counter({'gr_' + group: 1}) + \
        Counter({'pr_price': price}) + \
        Counter(['tag_' + tag for tag in tags])

    feature_list1.append(text_features_1)
    feature_list2.append(text_features_2)

v = DictVectorizer(sparse=True)
feature_set_1 = v.fit_transform(feature_list1)
feature_set_2 = v.fit_transform(feature_list2)

# COMBINE LABELS AND FEATURES
