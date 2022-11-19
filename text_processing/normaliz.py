from typing import List
import pymorphy2
from nltk.corpus import stopwords
from nlp_rake import Rake
from nltk import word_tokenize
from nltk.probability import FreqDist
import string
import nltk
nltk.download('punkt')

class TextStemManager:
    def bring_to_base_form(self, words: List[str]) -> List[str]:
        pass

class TextLemmingManager(TextStemManager):
    def __init__(self):
        self.__pymorphy = pymorphy2.MorphAnalyzer()
    def bring_to_base_form(self, words: List[str]) -> List[str]:
        for i in range(len(words)):
            words[i] = self.__pymorphy.parse(words[i])[0].normal_form
        return words

class TextCleaner:
    def clear_text(self, words: List[str]) -> List[str]:
        pass

class StopwordsCleaner(TextCleaner):
    def __init__(self):
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('russian'))
    def clear_text(self, words: List[str]) -> List[str]:
        return [x for x in words if x not in self.stop_words]

class NormalizedText:
    def __init__(self, words: List[str], significant_words: List[str], common_words: List[str]):
        self.__words = words
        self.__significant_words = significant_words
        self.__common_words = common_words
    def get_normalized_text(self):
        return ' '.join(self.__words)
    def get_common_words(self):
        return self.__common_words
    def get_significant_words(self):
        return self.__significant_words

class SignificantWordsSelecter:
    def find_significant_words(self, text: str) -> List[str]:
        pass

class RakeSignificantWordsSelecter(SignificantWordsSelecter):
    def __init__(self, stop):
        self.__count = 5
        self.__max_words = 2
        self.__stop = stop
    def find_significant_words(self, text: str) -> List[str]:
        rake = Rake(stopwords=self.__stop, max_words=self.__max_words)
        significant_words = rake.apply(text)
        common_significant_words = significant_words[0:self.__count]
        return [word for (word, percent) in common_significant_words]

class TextOperation:
    def normalize(self, text: str) -> NormalizedText:
        pass

class TextNormalizer(TextOperation):
    def __init__(self):
        self.__text_stem_manager = TextLemmingManager()
        self.__text_cleaner = StopwordsCleaner()
        self.__significant_words_selecter = RakeSignificantWordsSelecter(self.__text_cleaner.stop_words)
        self.__common_words_count = 5
    def normalize(self, text: str) -> NormalizedText:
        text_without_punctuation = text.translate(str.maketrans('', '', string.punctuation))
        tokenized = self.__tokenize(text_without_punctuation)
        clear_words = self.__text_cleaner.clear_text(tokenized)
        normalized = self.__text_stem_manager.bring_to_base_form(clear_words)
        common_words = self.__find_common_words(normalized)
        significant_words = self.__significant_words_selecter.find_significant_words(text)
        return NormalizedText(normalized, significant_words, common_words) 
    def __tokenize(self, text): 
        return word_tokenize(text.lower())
    def __find_common_words(self, words: List[str]):
        fdist = FreqDist(words)
        most_common = fdist.most_common(self.__common_words_count)
        return [word for (word, count) in most_common]