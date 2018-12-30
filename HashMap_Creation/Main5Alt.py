#!/usr/bin/python3

from HashMap import word_frequency
import re


def sanitize(word):
    return re.sub(r'[^\w\s]', '', word).lower()


def main(filename, words):
    with open(filename, 'r') as reader:
        freq = word_frequency(sanitize(word) for line in reader for word in line.split())
        print('unique words:', len(freq))
        for word in words:
            print(word, freq[word])


if __name__ == '__main__':
    main('romeojuliet.txt', ['romeo', 'juliet'])