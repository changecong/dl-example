#!/usr/bin/env python
# -*- coding: utf-8 -*-        

class WordMetadata:

    def __init__(self):
        self.__sentences = Sentences()
        self.__labeled_sentences = Labels()
        
    def add_metadata(self, sentences, labeled_sentences):
        if len(sentences) == len(labeled_sentences):
            self.__sentences.append_sentence(sentences)
            self.__labeled_sentences.append_labeled_sentence(labeled_sentences)
        else:
            # ignore
            pass
            
    def get_metadata(self):
        return self.__sentences, self.__labeled_sentences

    def is_empty(self):
        return self.__sentences.is_empty()
    
####
# helper classes
####

class Sentences:

    # constructor
    def __init__(self):
        # a list of sentences
        self.__sentences = []

    # public methods
    def append_sentence(self, sentence):
        self.__sentences.append(sentence)
        
    def get_sentences(self):
        return self.__sentences

    def get_sentence(self, idx, words=False):
        if (words):
            return self.__sentences[idx]
        else:
            return ' '.join(word for word in self.__sentences[idx])

    def is_empty(self):
        return len(self.__sentences) == 0
    # private methods

class Labels:
    

    # constructor
    def __init__(self):
        # a list of sentneces' labels
        self.__labeled_sentences = []

    # public methods                                                                                                                                                                                                
    def append_labeled_sentence(self, sentence):
        self.__labeled_sentences.append(sentence)

    # private methods    
    def get_labels(self):
        return self.__labeled_sentences

    def get_labeled_sentence(self, idx, label_list=False):
        if (label_list):
            return self.__labeled_sentences[idx]
        else:
            return ' '.join(label for label in self.__labeled_sentences[idx])

    def is_empty(self):
        return len(self.__labeled_sentences) == 0
