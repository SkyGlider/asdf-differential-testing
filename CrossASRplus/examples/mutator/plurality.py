from crossasr import Mutator
from crossasr import Text
from crossasr.utils import preprocess_text
import inflect
import nltk

from crossasr.constant import FAILED_TEST_CASE


# OPTIONAL: For error checking
# from gingerit.gingerit import GingerIt


class Pluralizer(Mutator):
    STOP_WORDS = nltk.corpus.stopwords.words('english')
    VALID_WORDS = nltk.corpus.words.words()

    def __init__(self, name="plurality"):
        super().__init__(name)
        self.inflect_engine = inflect.engine()

    def generate_mutated_sentences(self):
        """
        replace all the error words in the texts to homophone
        """
        mutated_sentences = []
        transcription_results = self.get_transcription_results()
        for i in range(len(transcription_results)):
            text = transcription_results[i].text
            transcriptions = transcription_results[i].transcriptions
            cases = transcription_results[i].cases
            filename = transcription_results[i].filename

            if FAILED_TEST_CASE in cases.values():

                error_words = self.get_all_error_words(text, transcriptions, cases)
                text_tokens = text.strip().split()
                print("Original:", text)

                for j, text_word in enumerate(text_tokens):
                    if text_word in error_words:
                        text_tokens[j] = self.get_plural(text_word)

                joined_sentence = " ".join(text_tokens).strip()
                print("Transformed:", joined_sentence)

                if text.strip() != joined_sentence:
                    mutated_sentences.append(Text(filename, joined_sentence))

        return mutated_sentences

    def get_plural(self, word: str):

        # Method 0 : Pluralise everything (even if words don't even exist)
        plural_word = self.inflect_engine.plural(word)
        singular_word = self.inflect_engine.singular_noun(word)
        if plural_word and word != plural_word:
            return plural_word.lower()
        elif singular_word and word != singular_word:
            return singular_word.lower()
        else:
            return word

        # Method 1 : Prevent translation fo stop words (fast)
        # if word.lower() in self.STOP_WORDS:
        #     return word
        # return self.inflect_engine.plural(word).lower()

        # Method 2 : Check plural or singular version of word, also check if word exists in english (slower)
        # plural_word = self.inflect_engine.plural(word)
        # singular_word = self.inflect_engine.singular_noun(word)
        # if plural_word and word != plural_word and plural_word in self.VALID_WORDS:
        #     return plural_word.lower()
        # elif singular_word and word != singular_word and singular_word in self.VALID_WORDS:
        #     return singular_word.lower()
        # else:
        #     return word

        # Method 3 : Check grammar AND spelling

    def get_all_error_words(self, text, transcriptions, cases):
        """
        get all error texts from transcriptions
        :returns: all_error_words []
        """

        def get_error_words(text, transcription):
            text_words = text.split()
            transcription_words = transcription.split()

            word_count = {}

            # Using dictionary to determine which word in the transcription doesn't exist in text
            for word in text_words:
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1

            for word in transcription_words:
                if word in word_count:
                    word_count[word] -= 1

            error_words = []
            for k in word_count.keys():
                if word_count[k] > 0:
                    error_words.append(k)

            return error_words

        all_error_words = []

        for k, transcription in transcriptions.items():
            case = cases[k]
            if case == 1 and transcription != "":
                error_words = get_error_words(text, transcription)
                all_error_words += error_words

        all_error_words = list(set(all_error_words))  # remove duplicates

        return all_error_words

    def get_error_words_per_asr(self, text, transcriptions, cases):
        """
        get error texts per asr from transcriptions
        :returns: asrs_error_words {asr: [error_words], ...}
        """

        def get_error_words(text, transcription):
            text_words = text.split()
            transcription_words = transcription.split()

            word_count = {}

            for word in text_words:
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1

            for word in transcription_words:
                if word in word_count:
                    word_count[word] -= 1

            error_words = []
            for k in word_count.keys():
                if word_count[k] > 0:
                    error_words.append(k)

            return error_words

        asrs_error_words = {}

        for k, transcription in transcriptions.items():
            case = cases[k]
            if case != 1:
                asrs_error_words[k] = []
            else:
                error_words = get_error_words(text, transcription)
                asrs_error_words[k] = error_words

        return asrs_error_words
