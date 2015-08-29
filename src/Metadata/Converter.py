#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim.models import Word2Vec
from Generator import TextDataReader
from Metadata import WordMetadata, VectorMetadata

import numpy

class VectorConverter:
    
    def __init__(self, vector_file_name):
        # binary vector file only
        self.__file_name = vector_file_name
        self.__gensim_model = None

    def __init_gensim_model(self):
        if self.__gensim_model is None:
            self.__gensim_model = Word2Vec.load_word2vec_format(\
                self.__file_name, binary=True)
            

    def convert_from_file(self, file_name):
        reader = TextDataReader(file_name)
        return self.convert_from_metadata(reader.get_metadata())

    
    def convert_from_metadata(self, word_metadata):
        self.__init_gensim_model()
        
        vector_metadata = VectorMetadata()

        sentences, labeled_sentences = word_metadata.get_metadata()

        sentences_list = sentences.get_sentences()
        labels_list = labeled_sentences.get_labels()
        
        for sentence, labeled_sentence in zip(sentences_list, labels_list):
            
            temp_sentence = []
            temp_labeled_sentence = []

            for idx in range(len(sentence)):
                if sentence[idx] in self.__gensim_model:
                    temp_sentence.append(self.__gensim_model[sentence[idx]])
                    temp_labeled_sentence.append(labeled_sentence[idx])
                                    
            if len(temp_sentence) != 0 and len(temp_labeled_sentence) != 0 and \
                    len(temp_sentence) == len(temp_labeled_sentence):
                vector_metadata.add_metadata(temp_sentence, temp_labeled_sentence)
                
        return vector_metadata


