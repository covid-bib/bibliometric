"""
based on https://github.com/miguelfzafra/Latest-News-Classifier/blob/master/0.%20Latest%20News%20Classifier/03.%20Feature%20Engineering/03.%20Feature%20Engineering.ipynb
"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

# A Scopus documents dataset with abstracts and membership of subject areas requred as input
# Due to Scopus copyright issues the dataset is not available on GitHub

df = pd.read_excel("abstracts for text mining and other properties.xlsx")
my_stop = np.loadtxt("additional_stop_words.txt", delimiter = '\n\n', dtype=str)

for c in ["\r", "\n", "    ", '"']:
    df["Abstract Parsed"] = df["Abstract"].str.replace(c, " ")

df["Abstract Parsed"] = df["Abstract Parsed"].str.lower()

punctuation_signs = list("?:!.,;%()•-©&")

for punct_sign in punctuation_signs:
    df["Abstract Parsed"] = df["Abstract Parsed"].str.replace(punct_sign, "")
    
df["Abstract Parsed"] = df["Abstract Parsed"].str.replace("'s", "")

wordnet_lemmatizer = WordNetLemmatizer()
stop_words = list(stopwords.words("english")) + list(my_stop)

nrows = len(df)
lemmatized_text_list = []

for row in range(0, nrows):  
    lemmatized_list = []   
    text = df.loc[row]["Abstract Parsed"]
    text_words = text.split(" ")
    for word in text_words:
        lemmatized_list.append(wordnet_lemmatizer.lemmatize(word)) 
    lemmatized_text = " ".join(lemmatized_list)   
    lemmatized_text_list.append(lemmatized_text)

df["Abstract Parsed"] = lemmatized_text_list

for stop_word in stop_words:
    try:
        regex_stopword = r"\b" + stop_word + r"\b"
        df["Abstract Parsed"] = df["Abstract Parsed"].str.replace(regex_stopword, "")
    except:
        print("Problem with", stop_word)

tfidf = TfidfVectorizer(encoding="utf-8", ngram_range=(1,2), stop_words=stop_words,
                        lowercase=False, max_df=1., min_df=10, max_features=100,
                        norm="l2", sublinear_tf=True)

features = tfidf.fit_transform(df["Abstract Parsed"]).toarray()

df_features = pd.DataFrame(features, columns=tfidf.get_feature_names())
for sa in ["Multidisciplinary", "Health Sciences", "Life Sciences", "Physical Sciences", "Social Sciences & Humanities"]:
    df_features[sa] = df[sa]

df_features.to_excel("dataset_for_classification.xlsx", index=False)