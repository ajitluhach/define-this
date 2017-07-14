from dictionary import Dictionary
from dictionary import SpellError
import sys
import argparse


base_url = 'https://od-api.oxforddictionaries.com:443/api/v1/'
app_id = "9f5bf14c"
app_key = "5f8f7d6089f3a734a78e4608b51d1fce"


def main():
    parser = argparse.ArgumentParser(description="A utility to give\
            definitions, synonyms, antonyms, examples of the given word.")
    parser.add_argument("word", help="Provide a word to define, or to get\
            synonyms, antonyms, and examples of")
    parser.add_argument("-e", "--full-entry", help="add this to get full entry\
            containing definitions, and examples of the word")
    parser.add_argument("-s", help="To get the synonym and \
            antonyms of the word")
    parser.add_argument("-x", "--examples", help="If you just want examples\
            of the word")
    parser.add_argument('-sent', '--sentences', help="Retrieve the sentences\
            for the given word")
    parser.add_argument("-l", "--limit", help="Limit of synonym, antonym, and\
            sentences(examples to get)", type=int, default=5)
    args = parser.parse_args()
    get = Dictionary(base_url, app_id, app_key)
    while True:
        try:
            if args.word:
                if args.full_entry:
                    get.entries(args.word)
                    get.syns_and_antons(args.word)
                elif args.examples:
                    get.examples(args.word)
                elif args.s:
                    get.syns_and_antons(args.word)
                else:
                    get.definitions(args.word)
            sys.exit()
        except (SpellError, Exception) as e:
            print(e)
            sys.exit()


if __name__ == '__main__':
    main()
