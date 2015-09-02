#!/usr/bin/env python
# -*- coding: utf-8 -*-

from generator import TextDataReader

text_data_reader = TextDataReader()
text_metadata = text_data_reader.get_metadata_from_word_data('data-example/labeled_words')
text_sentences, text_labels = text_metadata.get_metadata()

print "Label - Word pair"

while True:
    index = raw_input('please choose the sentence in a range of [0, ' + str(len(text_sentences.get_sentences())) + '), \'x\' to quit, \'all\' for all : ')

    if index == 'x':
        break
    elif index == 'all':
        counter = 0
        for sentence, labels in zip(text_sentences.get_sentences(), text_labels.get_labels()) :
            print str(counter), sentence
            print str(counter), labels
            counter = counter + 1
        break

    print 'Sentence :', text_sentences.get_sentences()[int(index)] 
    print 'Lables   :', text_labels.get_labels()[int(index)]

