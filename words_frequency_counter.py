from collections import Counter
from itertools import chain
from operator import itemgetter
from typing import Iterator, Generator
import re
import string

import requests

from report import generate_report


def get_words() -> Iterator:
    """Get data"""
    urls = ('https://storage.googleapis.com/apache-beam-samples/shakespeare/kinglear.txt',
            'https://storage.googleapis.com/apache-beam-samples/shakespeare/othello.txt',
            'https://storage.googleapis.com/apache-beam-samples/shakespeare/romeoandjuliet.txt')

    data_url = (requests.get(url).text.lower().split() for url in urls)
    data_url = chain.from_iterable(data_url)
    return data_url


def clean_words(data: Iterator) -> Generator:
    """Clean the data"""
    re_path = re.compile(f'[{re.escape(string.punctuation)}]')
    return (re_path.sub('', w) for w in data)


def get_relevant_words(words: Generator) -> Generator:
    """Get relevant words"""
    with open("StopWords.txt", "r") as file:
        stop_words = [word.strip() for word in file]
    return (x for x in words if x not in stop_words)


def word_frequency_counter(relevant_words: Generator) -> dict:
    """Count and analyze word frequencies"""
    count_word_freq = Counter(relevant_words)
    return dict(sorted(count_word_freq.items(), key=itemgetter(1), reverse=True))


def main():
    data_url = get_words()
    words = clean_words(data_url)
    relevant_words = get_relevant_words(words)
    generate_report(word_frequency_counter(relevant_words))


if __name__ == '__main__':
    main()
