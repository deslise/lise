import re

from cogroo_interface import Cogroo
from googleapiclient.discovery import build


class Organization(object):

    def __init__(self):
        self.cogroo = Cogroo.Instance()

    def separate_sentences(self, text):
        sentence_delimiters = re.compile(u'[.!?,;\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s| mas | porem | pois | no entanto')
        sentences = sentence_delimiters.split(text)
        return sentences

    def all_separate_sentences(self, reviews):
        sentences = []
        for review in reviews:
            sentences += self.separate_sentences(review.complete_text)
        return sentences

    def load_stop_words(self, stop_word_file):
        stop_words = []
        for line in open(stop_word_file):
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
        return stop_words

    def pattern_regex(self, stop_word_file_path):
        stop_word_list = self.load_stop_words(stop_word_file_path)
        stop_word_regex_list = []
        for word in stop_word_list:
            word_regex = r'\b' + word + r'(?![\w-])'  # added look ahead for hyphen
            stop_word_regex_list.append(word_regex)
        stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
        return stop_word_pattern

    def remove_verbs(self, tokens, phrase):
        for word in tokens:
            if word.pos == 'v-fin':
                person = word.feat.split('=')[1]
                if person == '1S' or word.lemma == 'ser':
                    phrase = phrase.replace(word.lexeme, '')
        return phrase


    def clean_sentence(self, sentence, pattern_regex):
        phrase = re.sub(pattern_regex, '', sentence.strip())
        tokens = self.tokens_cogroo(phrase)
        if self.validate_sentence(tokens):
            words = self.remove_verbs(tokens, phrase).split()
            if len(words) > 1:
                return ' '.join(words).capitalize()
        return False


    def validate_sentence(self, tokens):
        pos = list(map(lambda x: x.pos, tokens))
        return 'n' in pos and 'adj' in pos


    def tokens_cogroo(self, phrase):
        sentence = self.cogroo.analyze(' '.join(phrase.split())).sentences or False
        tokens = sentence[0].tokens if sentence else []
        return tokens


    def generate_keywords(self, sentence_list, pattern_regex):
        self.service = build('translate', 'v2', developerKey='AIzaSyB0UBbtTXcMS8DrdviSLxab9Oa0B_Dcclg')
        phrase_list = {}
        for sentence in sentence_list:
            sentence = self.clean_sentence(sentence, pattern_regex)
            if sentence:
                phrase_list[self.translate(sentence)] = sentence
        return phrase_list

    def translate(self, frase, lang='en'):
        return self.service.translations().list(source='pt', target=lang, q=frase).execute()['translations'][0][
            'translatedText']
