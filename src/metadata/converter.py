#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim.models import Word2Vec
from generator import TextDataReader
from metadata import WordMetadata, VectorMetadata

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

    def save_metadata_to_file(self, vector_metadata, file_name, append=False):

        if isinstance(vector_metadata, VectorMetadata):
            vector_sentences, labeled_sentences = vector_metadata.get_metadata()
            vectors = vector_sentences.get_sentences() # list
            labels = labeled_sentences.get_labels() # list
            
            if len(vectors) == len(labels) and \
                    len(vectors) != 0 and len(labels) != 0:
                
                way_to_opend = ''
                if append:
                    way_to_open = 'a'
                else:
                    way_to_open = 'w'

                output_file = open(file_name, way_to_open)

                for vector_sentence, labeled_sentence in zip(vectors, labels):
                    output_file.write('#\n') # indicates a sentence
                    for vector, label in zip(vector_sentence, labeled_sentence):
                        output_file.write(label.encode('utf-8') + ' ')
                         # '1.8e' accuracy is 1.8f 'e' means using scientific notation
                        output_file.write(' '.join('%1.8e' % number for number in vector))
                        output_file.write('\n')

                output_file.close()
                    
