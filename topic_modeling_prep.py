from dataaccess import *
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation
from nltk.tokenize import RegexpTokenizer
import heapq
import csv


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print (" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))

all_keys = get_keys()

month_number = {
    'Jan': '1',
    'Feb': '2',
    'Mar': '3',
    'Apr': '4',
    'May': '5',
    'Jun': '6',
    'Jul': '7',
    'Aug': '8',
    'Sep': '9',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

month_groups = [eval(key)['date'].split()[2] + ' ' + month_number[(eval(key)['date'].split())[1]] for key in all_keys if eval(key)['date'] != "Invalid"]

groups_count = Counter(month_groups)

# radimo za tri meseca u 2017

targets = ['Jan 2017', 'Feb 2017', 'Mar 2017']

target_key_groups = {target: [keys for keys in all_keys if target in eval(keys)['date']] for target in targets}

target_posts = {target: [' '.join(get(eval(key))['post']) for key in target_key_groups[target]] for target in targets}

tokenizer = RegexpTokenizer(r'\w+')


# USECASE 1 # EXPLORING NEW TOPICS
for target in targets:
    print()
    print("GROUP: ", target)
    data = target_posts[target]
    data = [document.lower() for document in data]
    data = [' '.join(tokenizer.tokenize(document)) for document in data]

    # NMF is able to use tf-idf
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform(data)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tf = tf_vectorizer.fit_transform(data)
    tf_feature_names = tf_vectorizer.get_feature_names()

    no_topics = 10

    # Run NMF
    nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

    # Run LDA
    lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,
                                    random_state=0).fit(tf)

    no_top_words = 10
    print('NMF: ')
    #display_topics(nmf, tfidf_feature_names, no_top_words)
    print('LDA: ')
    #display_topics(lda, tf_feature_names, no_top_words)

# USECASE 2 # FOLOWING TRENDS TROUGH TIME

data = [target_posts[target] for target in targets]
data = [item for sublist in data for item in sublist]
data = [document.lower() for document in data]
data = [' '.join(tokenizer.tokenize(document)) for document in data]

# NMF is able to use tf-idf
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(data)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
tf = tf_vectorizer.fit_transform(data)
tf_feature_names = tf_vectorizer.get_feature_names()

no_topics = 10

# Run LDA
lda_transformed = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit_transform(tf)
lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)

all_results = [heapq.nlargest(1, range(len(example)), key=example.__getitem__)[0] for example in lda_transformed]
month_sizes = [len(target_posts[target]) for target in targets]
month1 = [0, month_sizes[0] - 1]
month2 = [month_sizes[0], month_sizes[0] + month_sizes[1] - 1]
month3 = [month_sizes[0] + month_sizes[1], month_sizes[0] + month_sizes[1] + month_sizes[2] - 1]
month_limits = {targets[0]: month1, targets[1]: month2, targets[2]: month3}
month_results = {target: [result for idx, result in enumerate(all_results) if idx >= month_limits[target][0] and idx <= month_limits[target][1]] for target in targets}
month_results_counts = {target: Counter(month_results[target]) for target in month_results.keys()}
topics = {topic_idx: " ".join([tf_feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]) for topic_idx, topic in enumerate(lda.components_)}

with open('results.csv', 'w') as csvfile:
    reswriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    reswriter.writerow(['target', 'topic', 'count'])
    for target in targets:
        for topic_idx, freq in month_results_counts[target].most_common():
            reswriter.writerow([target, topics[topic_idx], freq])

