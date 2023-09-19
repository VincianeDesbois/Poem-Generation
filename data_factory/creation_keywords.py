import os
import re
import string
from collections import Counter
from pathlib import Path

import pandas as pd
import stanza
import tqdm
from webscrapped_poem_cleaning import clean_dataframe

stanza.download("fr")
nlp = stanza.Pipeline(lang="fr", processors="tokenize,mwt,pos,lemma,depparse")


def key_words(s):
    """
    List 3 important words in a verse from webscrapped poems.

    Parameters
    ----------
    s: string
       One verse of a webscrapped poem.

    Returns
    -------
    list
        List of 3 strings corresponding to 3 important words in the input s.
    """
    list_words = []

    if len(get_imp_words(s, 0)) < 3:
        if len(nlp(s).sentences) == 2:
            list_words = get_imp_words(s, 0) + get_imp_words(s, 1)
        else:
            list_words = get_imp_words(s, 0) + get_adj_adv(s)
        list_words = list_words[:3]
    else:
        list_words = get_imp_words(s, 0)
    return list_words


def get_imp_words(txt, i):
    """
    Extract 3 (at most) head words of a verse from webscrapped poems.

    Parameters
    ----------
    txt: string
         One verse of a webscrapped poem.
    i: int
       Position of the sentence studied inside the verse (only 0 or 1).

    Returns
    -------
    list
        List of 3 (or less) strings corresponding to the head words of the verse.
    """

    # tag the sentences
    doc = nlp(clean_text(txt))
    sent = doc.sentences
    list_head = []
    imp_words = []
    imp_words_lemma = []

    for w in sent[i].words:
        if w.head == 0:  # is the root-word of the sentence
            imp_words.append(w.text)
            imp_words_lemma.append(w.lemma.lower())
        list_head.append(
            w.head
        )  # append the position of the word considered as "head word" of w
    list_head.remove(0)

    count_ = Counter(list_head)
    for com in count_.most_common(4):
        # we make a list of the most common "head words"
        imp_words.append(sent[i].words[com[0] - 1].text)
        imp_words_lemma.append(sent[i].words[com[0] - 1].lemma.lower())

    imp_words_lemma = list(set(imp_words_lemma))
    try:
        imp_words_lemma = imp_words_lemma[:3]
    except:
        pass

    return imp_words_lemma


def clean_text(txt):
    """
    Remove punctuation in a given text.

    Parameters
    ----------
    txt: string
         One verse of a webscrapped poem

    Returns
    -------
    string
         Same text without any punctuation.
    """
    txt = re.sub("'|-", " ", txt)
    punct = string.punctuation
    for c in punct:
        txt = txt.replace(c, "")
    return txt


def get_adj_adv(s):
    """
    Create a list of the possible adjectives and adverbs of a given sentence.

    Parameters
    ----------
    s: string
       One verse of a webscrapped poem.

    Returns
    -------
    list
       List of strings (adjectives or adverbs present in the verse)
    """
    w_lemma = []
    for w in nlp(s).sentences[0].words:
        if w.upos == "ADJ":
            w_lemma.append(w.lemma.lower())
    for w in nlp(s).sentences[0].words:
        if w.upos == "ADV":
            w_lemma.append(w.lemma.lower())
    return w_lemma


# We apply our functions on the webscrapped poems to create the training dataset of our model

# cwd = Path(os.path.dirname(os.path.realpath(__file__)))
# path = cwd.parent
# df = pd.read_csv(cwd / "data_dataset_poems.csv")

# dfc = clean_dataframe(df)
# dfc['key_words']= 0

# for row in tqdm(range(len(dfc))):
#    try:
#       s = dfc['text'][row]
#      dfc['key_words'][row] = key_words(s)
# except:
#    pass

# dfc.to_csv(cwd / "df_key_words.csv")
