from itertools import chain
from operator import itemgetter
import re
import string

import requests

urls = ('https://storage.googleapis.com/apache-beam-samples/shakespeare/kinglear.txt',
        'https://storage.googleapis.com/apache-beam-samples/shakespeare/othello.txt',
        'https://storage.googleapis.com/apache-beam-samples/shakespeare/romeoandjuliet.txt')

data_url = (requests.get(url).text.lower().split() for url in urls)  # Get urls data and convert in words lists
data_url = chain.from_iterable(data_url)  # Join three iterable words lists in only one.


def clean_words(data):
    """Clean the data, punctuation and irrelevant words"""
    re_path = re.compile(f'[{re.escape(string.punctuation)}]')  # regex pattern
    words_clean_p = (re_path.sub('', w) for w in data)  # Clean punctuation

    with open("StopWords.txt", "r") as f:
        stop_words = [word.strip() for word in f]  # Get stop words data to relevant words classification
    relevant_words = [x for x in words_clean_p if x not in stop_words]  # Get only relevant words

    return relevant_words


def word_frequency_counter(words):
    """Count and analyze word frequencies"""
    count_word_freq = (words.count(word) for word in words)  # Count words frequency
    freq_word_dic = dict(zip(words, count_word_freq))  # Convert the frequency list and word list in Dict

    return dict(sorted(freq_word_dic.items(), key=itemgetter(1), reverse=True))  # Dict ordered by frequency (gtl)


dic = word_frequency_counter(clean_words(data_url))

# Template HTML Table Listing Report.
table_base = f"""<style>
    .i-am-centered {{ margin: auto; max-width: 800px;}}
    table .alto {{background-color:gray;}}
    </style>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <br>
    <div class="i-am-centered">
    <div class="row">
    <div class="col-lg-8 col-md-8 col-sm-8 col-xs-8">
    <h2>Shakespeare's Research</h2>
    <hr>
    <table class="table table-hover table-bordered">
    <caption>{len(dic)} Relevant words in three Shakespeare's literary masterpieces.</caption>
    <thead><tr><th class="alto" scope="col">Words</th><th class="alto" scope="col">Frecuency</th></tr></thead><tbody>"""

if __name__ == '__main__':
    # Create a HTML Table Listing Report.
    for w, f in dic.items():
        table_item = f'<tr><th> {str(w)} </th><th> {str(f)} </td></tr>'
        table_base = table_base + table_item

    table_base = f'{table_base}</tbody></table></div></div></div></div>'

    with open("word_frequencies_report.html", "w") as file:
        file.write(table_base)
