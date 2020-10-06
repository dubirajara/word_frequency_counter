from collections import Counter
from itertools import chain
from operator import itemgetter
from typing import Iterator
import re
import string

import requests

from report import generate_report

urls = ('https://storage.googleapis.com/apache-beam-samples/shakespeare/kinglear.txt',
        'https://storage.googleapis.com/apache-beam-samples/shakespeare/othello.txt',
        'https://storage.googleapis.com/apache-beam-samples/shakespeare/romeoandjuliet.txt')

data_url = (requests.get(url).text.lower().split() for url in urls)  # Get urls data and convert in words lists
data_url = chain.from_iterable(data_url)  # Join three iterable words lists in only one.


def clean_words(data: Iterator) -> list:
    """Clean the data, punctuation and irrelevant words"""
    re_path = re.compile(f'[{re.escape(string.punctuation)}]')  # regex pattern
    words_clean_p = (re_path.sub('', w) for w in data)  # Clean punctuation

    with open("StopWords.txt", "r") as file:
        stop_words = [word.strip() for word in file]  # Get stop words data to relevant words classification
    relevant_words = [x for x in words_clean_p if x not in stop_words]  # Get only relevant words

    return relevant_words


def word_frequency_counter(words: list) -> dict:
    """Count and analyze word frequencies"""
    count_word_freq = Counter(words)
    return dict(sorted(count_word_freq.items(), key=itemgetter(1), reverse=True))  # Dict ordered by frequency (gtl)


if __name__ == '__main__':
    generate_report(word_frequency_counter(clean_words(data_url)))
