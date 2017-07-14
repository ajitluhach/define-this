from oxfordapi import OxfordAPI
import os
import json


endc = '\033[0m'
bold = '\033[01m'
BLACK = '\33[30m'
RED = '\33[31m'
GREEN = '\33[32m'
YELLOW = '\33[33m'
BLUE = '\33[34m'
VIOLET = '\33[35m'
BEIGE = '\33[36m'
WHITE = '\33[37m'


class SpellError(Exception):
    pass


class Dictionary(OxfordAPI):
    """Inherits the method to interact with Oxford API's from class, OxfordAPI

    Refines the response generated by the API's for user view.
    """
    def __init__(self, url, app_id=None, app_key=None):
        self.app_id = app_id
        self.app_key = app_key
        super().__init__(url, self.app_key, self.app_id)

    def _parse_response(self, response):
        parsed_json = json.loads(response.text)
        results = parsed_json["results"][0]
        lexicals = results['lexicalEntries']
        self._handle_lexical_entries(lexicals)

    def _handle_lexical_entries(self, lexicals):
        """
        lexicals: Containing a list of lexical entries

        each lexical has a category, which is to be the head of that entry.
        also incooperates `entries` which is a list of senses
        """
        for lexical in lexicals:
            width = os.get_terminal_size().columns
            print(width*'-')
            category = lexical["lexicalCategory"]
            print(YELLOW + "Category: " + category + endc)
            entries = lexical["entries"]
            self._handle_entries(entries)
        print(width*'-')

    def _handle_entries(self, entries):
        """
        entries:  List of dictionaries containing following entries about
                  any word.
        A single Entry has:
            lexicalCategory: Category of the word
            pronunciations: a list of dictionary containing following keys
                            audioFile(mp3), dialects(list)
            etymologies: a list of etymologies
            senses: a list of dictionaries
        """
        for entry in entries:
            senses = entry["senses"]
            self._handle_senses(senses)

    def _handle_senses(self, senses):
        """
        senses: a list containing, definitions, examples, and other things
        """
        for sense in senses:
            self._sense(sense)

    def _print_keyword(self, iterable, key='', indent=0, color=None):
        indent = indent*4
        for num, item in enumerate(iterable):
            if key:
                item = item["text"]
            print(color + indent*' ' + "- " + item + endc)

    def _print_in_one_line(self, iterable, indent=0, color=None):
        indent *= 4
        string = ', '.join(x["text"] for x in iterable)
        print(color + indent*' ' + "-" + string + endc + "\n")

    def _sense(self, sense):
        """
        A list of dictionaries containin following fields
        :domains        a list of domains
        :definitions    a list of definitions
        :examples       contains a list of dictionaries,  keys `text`
        :subsense       similar to sense

        """
        indent = 1
        if "domains" in sense:
            domains = sense["domains"]  # a list of domains, have to printing
            domains = ', '.join(domain for domain in domains)
            print(VIOLET + "Domains: " + domains + endc)

        if "definitions" in sense:
            print(GREEN + "Definition: " + endc)  # add color to it
            definitions = sense["definitions"]  # a list of definitions
            indent += 1
            self._print_keyword(iterable=definitions, indent=indent,
                                color=GREEN)
        if "synonyms" in sense:
            print(BEIGE + "Synonym:" + endc)
            synonyms = sense["synonyms"]
            indent += 1
            self._print_in_one_line(iterable=synonyms, indent=indent,
                                    color=BEIGE)

        if "antonyms" in sense:
            print(WHITE + "Antonym:" + endc)
            antonyms = sense["antonyms"]
            self._print_in_one_line(iterable=antonyms, indent=indent,
                                    color=WHITE)
        if "examples" in sense:
            print(indent*'  ' + BLUE + "Example: " + endc)
            indent += 1
            examples = sense["examples"]  # a list of examples
            self._print_keyword(iterable=examples, key="text",
                                indent=indent, color=BLUE)
        if "subsenses" in sense:
            self._sense(sense["subsenses"])

    def definitions(self, word):
        response = self._get_definitions(word)
        if self._everything_good(response):
            self._parse_response(response)

    def examples(self, word):
        response = self._get_examples(word)
        if self._everything_good:
            self._parse_response(response)

    def syns_and_antons(self, word):
        response = self._get_syns_antons(word)
        if self._everything_good:
            self._parse_response(response)

    def search(self, query, limit=6):
        self._do_search(query, limit)
        pass

    def entries(self, word):
        response = self._get_entries(word)
        if self._everything_good:
            raise SpellError
        self._parse_response(response)

    def _everything_good(self, response):
        status_code = response.status_code
        if status_code == 200:
            return True
        elif status_code == 404:
            raise SpellError("SpellError, word not found")
        else:
            raise Exception("Something went wrong, it's not a spell error")