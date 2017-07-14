from collections import Counter
import re
import csv


def words(text):
    return re.findall(r"(?<!')(\w{2,})", text.lower())


def main():
    TRAINED_WORDS = open('trained_words.txt').read()
    TRAINED_WORDS = Counter(words(TRAINED_WORDS))
    REAL_WORDS = Counter(words(open('dictionary.txt').read()))
    print("MOST COMMON TEN Words {}".format(TRAINED_WORDS.most_common(15)))
    with open("trained_words.csv", 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in TRAINED_WORDS.items():
            print(key, value)
            writer.writerow([key, value])

    with open("real_words.csv", 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in REAL_WORDS.items():
            writer.writerow([key, value])


if __name__ == '__main__':
    main()
