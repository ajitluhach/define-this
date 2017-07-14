from collections import Counter
import re
import os
import json


def words(text):
    return re.findall(r"(?<!')(\w+)", text.lower())


def describe(words):
    print("Totatl Words: {}\n Words: {}, ".format(len(words.keys()), sum(words.values())))


def train_from_files(data):
    word_list = []
    for root, dirs, files in os.walk(data):
        # print(root)
        for file in files:
            if file.endswith(".txt"):
                file = os.path.join(root, file)
                with open(file, 'r') as r:
                    word_list.extend(words(r.read()))

    TRAINED_WORDS = Counter(word_list)
    print("Uncleaned Words :")
    describe(TRAINED_WORDS)
    return word_list  # because it would be easy to count them later


def real_words(location="/usr/share/dict/words"):
    word_list = []
    with open(location, "r") as r:
        word_list = words(r.read())
    real_words = Counter(word_list)
    return real_words  # for each check in of containment


def main():
    current = os.getcwd()
    data = current + "/data"
    trained = train_from_files(data)  # list
    real = real_words()  # dictionary

    purified_train = [x for x in trained if x in real.keys()]
    with open("trained_words.txt", 'w+') as w:
        purified = Counter(purified_train)
        w.write(' '.join(purified_train))
        print("Cleaned Used Words")
        describe(purified)
    with open('dictionary.txt', 'w+') as w:
        w.write(' '.join(real))
        print("Real dictionary words ")
        describe(real)


if __name__ == "__main__":
    main()
