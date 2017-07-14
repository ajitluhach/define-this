import csv
from collections import Counter
from itertools import imap, product


class SpellChecker:
    def __init__(self):
        self.REAL = set(self._make_counter("real_words.csv"))
        self.TRAINED = self._make_counter("trained_words.csv")
        self.vowels = set('aeiouy')
        self.alphabet = set('abcdefghijklmnopqrstuvwxyz')

    def _frequency(self, word, model):
        return model.get(word, 0)

    def _P(self, word):
        return self._frequency(word)/sum(self.TRAINED.values)

    def _make_counter(self, csv_file):
        """Return a counter dictionary for the csv file,
        which is assumed to contain key,value pairs of the word and
        it's occurence
        """
        with open(csv_file, "r") as r:
            reader = csv.reader(r)
            WORDS = Counter()
            for row in reader:
                WORDS[row[0]] = int(row[1])
        return WORDS

    def editdistance(self, word):
        """Get all the editdistance of a word
            splits: the word in different parts, of left and right
            deletes: generates new words by deleting a few letters
            replaces: list of words after replacemetns with alphabets
            inserts: list of words after insertion of new letter, b/w splits
            return a set of all the possible editdistance of the word
        """
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + a + R[1:] for L, R in splits for a in alphabet if R]
        inserts    = [L + a + R for L, R in splits for a in alphabet]
        return set(deletes + transposes + replaces + inserts)

    def hamming_distance(self, word1, word2):
        if word1 == word2:
            return 0
        dist = sum(imap(str.__ne__, word1[:len(word2)], word2[:len(word1)]))
        dist = max([word2, word1]) if not dist else dist+abs(len(word2) - len(word1))
        return dist

    def editdistance2(self, word):
        """Return the editdistance of the editdistance of the word."""
        return set(s for w in self.editdistance(word) for s in self.editdistance(w))

    def numberofdupes(self, word, idx):
        """Return the number of times the letter at index idx is repeated in
            the word
        """
        initial = idx
        w = word[idx]  # word at index idx
        # while next index is less then the length of word and same as previous
        while idx + 1 < len(word) and word[idx+1] == w:
            idx += 1
        return idx - initial

    def reductions(self, word):
        """Return list of all possible variations of the word by removing
            repeating word, that is reduce the word
        """
        word = list(word)
        for idx, l in enumerate(word):
            n = self.numberofdupes(word, idx)  # number of duplicates in the word
            # of the letter at current index
            # if there are any duplicates
            if n:
                # generate a list of possible removals of the letters
                dupes = [l*(r+1) for r in range(n+1)[:3]]  # take 3

                for _ in range(n):
                    word.pop(idx+1)
                word[idx] = dupes
        # generate seperate words for the 2d list
        for p in product(*word):
            yield ''.join(p)

    def vowelswaps(self, word):
        """Return a list of all possible vowelswaps for the given word"""
        word = list(word)
        # ['h','i'] becomes ['h', ['a', 'e', 'i', 'o', 'u', 'y']]
        for idx, l in enumerate(word):
            if type(l) == list:
                pass                        # dont mess with the reductions
            elif l in self.vowels:
                word[idx] = list(self.vowels)    # if l is a vowel, replace with all possible vowels

        # ['h',['i','ii','iii']] becomes 'hi','hii','hiii'
        for p in product(*word):
            yield ''.join(p)

    def both(self, word):
        """permute all combinations of reductions and vowelswaps"""
        for reduction in self.reductions(word):
            for variant in self.vowelswaps(reduction):
                yield variant

    def _suggestions(self, word):
        """Get all the spelling suggestions of a word"""
        return ({word}                          & self.REAL or   #  caps     "inSIDE" => "inside"
                set(self.reductions(word))      & self.REAL or   #  repeats  "jjoobbb" => "job"
                set(self.vowelswaps(word))      & self.REAL or   #  vowels   "weke" => "wake"
                set(self.editdistance(word))    & self.REAL or   #  other    "nonster" => "monster"
                set(self.both(word))            & self.REAL or   #  both     "CUNsperrICY" => "conspiracy"
                set(self.editdistance2(word))   & self.REAL or   #  other    "nmnster" => "manster"
                {"NO SUGGESTION"})

    def best(self, word, suggestions):
        """choose the best selection in the list of suggestions
            based on their hamming distance from the word, or 
            Probability of the edited word
        """
        suggestions = list(suggestions)

