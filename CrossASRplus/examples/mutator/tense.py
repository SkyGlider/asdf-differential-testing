import spacy
import pyinflect# importing sys
import sys

from crossasr import Mutator
from crossasr import Text
from crossasr.constant import FAILED_TEST_CASE, INDETERMINABLE_TEST_CASE

class Tense(Mutator):

    def __init__(self, name="tense"):
        super().__init__(name)
        # init spaCy pipeline
        self.model = spacy.load("en_core_web_sm")

    def generate_mutated_sentences(self):
        """
        replace all verbs in text with past tense
        """
        mutated_sentences = []
        transcription_results = self.get_transcription_results()
        for i in range(len(transcription_results)): 
            text = transcription_results[i].text
            transcriptions = transcription_results[i].transcriptions
            cases = transcription_results[i].cases
            filename = transcription_results[i].filename

            if FAILED_TEST_CASE in cases.values() :
                new_sentence = self.transform_tense(text)

                # no plurals and new sentence is different
                if (new_sentence is not None) and (new_sentence != text):
                    mutated_sentences.append(Text(filename, new_sentence))
        return mutated_sentences

    def transform_tense(self, text: str):
        doc_dep = self.model(text)
        for i in range(len(doc_dep)):
            token = doc_dep[i]
            # plural noun, not supported by spaCy
            # if token.tag_ in ['NNS']:
            #     return 
            # non-3rd person present singular verb, 3rd person present singular verb 
            if token.tag_ in ['VBP', 'VBZ']:
                text = text.replace(' '+token.text+' ', ' '+token._.inflect("VBD")+' ')
        return text
        