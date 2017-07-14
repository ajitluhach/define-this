import requests


class OxfordAPI:
    """An api wrapper over oxford dictionary api."""

    def __init__(self, url, app_key=None, app_id=None):
        """Initialize headers and base url"""
        self.base_url = url
        self._headers = {'app_key': app_key, 'app_id': app_id}

    def _get_response(self, url):
        response = requests.get(url, headers=self._headers)
        return response

    def _generate_url(self, head="entries", lang="en", word="",
                      get="definitions"):
        if get:
            get = "/" + get
        url = self.base_url + head + '/' + lang + "/" + word + get
        return url

    def _get_syns_antons(self, word):
        url = self._generate_url(word=word, get="synonyms;antonyms")
        response = self._get_response(url)
        return response

    def _do_search(self, query, limit):
        get = '?prefix=false' + "&limit=" + str(limit)
        url = self._generate_url(head='search', word=query, get=get)
        response = self._get_response(url)
        return response

    def _get_entries(self, word):
        url = self._generate_url(word=word, get="")
        response = self._get_response(url)
        return response

    def _get_examples(self, word):
        url = self._generate_url(word=word, get="examples")
        return self._get_response(url)

    def _get_definitions(self, word):
        url = self._generate_url(word=word, get="definitions")
        return self._get_response(url)
