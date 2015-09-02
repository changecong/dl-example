#!/usr/bin/env python
# -*- coding: utf-8 -*-

from generator import TextDataReader

text_data_reader = TextDataReader()
vector_metadata = text_data_reader.get_metadata_from_vector_data('data-example/labeled_vectors')
vector_sentences, vector_labels = vector_metadata.get_metadata()

print "Label - Vector pair"

while True:
    
    number = raw_input('please enter a number in a range of [0, ' + str(len(vector_sentences.get_sentences())) + '), \'x\' to quit : ')

    if number == 'x':
        break;

    sentence = vector_sentences.get_sentences()[int(number)]
    labeled_sentence = vector_labels.get_labels()[int(number)]
    
    index = raw_input('please enter a number in a range of [0, ' + str(len(sentence)) + '), \'x\' to quit : ')
    
    if index == 'x':
        break;
    
    print 'Word  :', '%1.8e' % sentence[int(index)]
    print 'Label :', labeled_sentence[int(index)]
