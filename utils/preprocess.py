import string
import nltk

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

ps = PorterStemmer()

STOP_WORDS = set(stopwords.words("english"))


def transform_text(text):

    text = text.lower()

    text = nltk.word_tokenize(text)

    words = []

    for word in text:

        if word.isalnum():
            words.append(word)

    filtered = []

    for word in words:

        if word not in STOP_WORDS and word not in string.punctuation:
            filtered.append(ps.stem(word))

    return " ".join(filtered)