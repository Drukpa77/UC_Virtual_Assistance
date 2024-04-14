import string
from nltk import word_tokenize as lib_tokenizer
import re

def strip_context(text):
    try:
      text = text.replace('\n', ' ')
    except:
      raise ValueError(text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def preprocess_text(x: str, max_length=-1, remove_puncts=False):
    x = nltk_tokenize(x)
    x = x.replace("\n", " ")
    if remove_puncts:
        x = "".join([i for i in x if i not in string.punctuation])
    if max_length > 0:
        x = " ".join(x.split()[:max_length])
    return x

def nltk_tokenize(x):
    return " ".join(word_tokenize(strip_context(x))).strip()

def word_tokenize(text):
    dict_map = dict({})
    words = text.split()
    words_norm = []
    for w in words:
        if dict_map.get(w, None) is None:
            dict_map[w] = ' '.join(lib_tokenizer(w)).replace('``', '"').replace("''", '"')
        words_norm.append(dict_map[w])
    return words_norm
