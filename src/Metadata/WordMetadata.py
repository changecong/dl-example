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
