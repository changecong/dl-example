#!/usr/bin/env python
# -*- coding: utf-8 -*-        

from lxml import etree
from metadata import WordMetadata, VectorMetadata

import xml.etree.ElementTree as ET
import numpy

class XMLDataReader:

    def __init__(self, file_name):
        self.__tree = etree.parse(file_name)
        self.__root = self.__tree.getroot()
        self.__tags_element = self.__root.findall('TAGS')[0]
        self.__text_element = self.__root.findall('TEXT')[0]

    def __get_tags_by_name(self, tag_name):

        # get all tag whose name is <tag_name>
        tags = self.__tags_element.findall(tag_name)
 
        tags_dict = {}
        for tag in tags:
            temp_tag = Tag(tag)
            tags_dict[temp_tag.index] = temp_tag

        return tags_dict

    def get_all_tags(self, tag_list):
        # return a dictionary of Tags, the key is the start position of each label

        all_tags = {}

        for tag in tag_list:
            tags_dict = self.__get_tags_by_name(tag)
            all_tags.update(tags_dict)

        return all_tags
            
    def get_text(self):
        # get text from CDATA

        return self.__text_element.text

    def label_sentences(self, text, tags):
        # this method does following things:
        # 1. skips suid=xxx participant=xxxxxx, since it isn't considered as a sentence
        # 2. splits text to sentences by newline
        # 3. label each word
    
        magic_word = "*pro*"
        stupid_word = "suid"
        
        # first pass
        # 1. remove stupid lines
        # 2. add start point of each sentence
        # [10, 'haha ni ge sha gua', 29, 'sha zi']
        
        sentences_and_positions = [0]

        # newlines are removed during the split we should still count them on generating positions
        for sentence in text.splitlines():
            if stupid_word in sentence:
                if len(sentences_and_positions) == 0:
                    # ideally this line won't be hit
                    sentences_and_positions.append(len(sentence) + 2)
                elif len(sentences_and_positions) % 2 == 1:
                    sentences_and_positions[-1] = sentences_and_positions[-1] + \
                                                  len(sentence) + 2
                else:
                    sentences_and_positions.append(sentences_and_positions[-2] + \
                                                   len(sentences_and_positions[-1]) + \
                                                   len(sentence) + 2)            
            else:
                sentences_and_positions.append(sentence)

        # second pass
        metadata = WordMetadata()

        for i in range(1, len(sentences_and_positions)):

            # get current sentence
            temp_sentence = sentences_and_positions[i]

            # if it isn't a string or empty, then ignore
            if isinstance(temp_sentence, basestring) and len(temp_sentence) != 0:
                # get its start position
                # since the first element is always 0, i - 1 is safe to be used withou check
                start_position = sentences_and_positions[i - 1]

                # splits string to a list of words
                temp_words = temp_sentence.split()

                # generates a list of labels, initializes with 'NA'
                temp_labels = ['NA'] * len(temp_words)

                # find the first magic_words index
                index = temp_sentence.find(magic_word)
                count = 0
                label_index = 0

                while index != -1:

                    lable = ""

                    # way to calculate the position of magic word
                    # <start position> + index + 1
                    if tags.get(str(start_position + index + 1), False):
                        label = tags[str(start_position + index + 1)].tag
                    else:
                        label = "NA"

                    try:
                        label_index = temp_words.index(magic_word, count)
                        temp_labels[label_index] = magic_word
                        if label_index < len(temp_labels) - 1 and temp_words[label_index + 1] != magic_word:
                            temp_labels[label_index + 1] = label

                            # sentence ["*pro*", "shi", "shui"]
                            # label    ["*pro*", "ni", "NA"]
                    except ValueError:
                        pass
                        
                    count = label_index + 1
                    index = temp_sentence.find(magic_word, index + 1)
                    
                temp_words = list(filter(lambda word: word != magic_word, temp_words))
                temp_labels = list(filter(lambda label: label != magic_word, temp_labels))
            
                metadata.add_metadata(temp_words, temp_labels)                

        return metadata

    def generate_text_file(self, metadata, file_name, append=False, offset=0):
        # write data into a text file with following format
        # id   content  type
        #  0 shi ge zhu   s
        #  0 ni NA NA     l
        #  1 cai shi zhu  s
        #  1 ni NA NA     l
        
        way_to_open = ''
        if append:
            way_to_open='a'
        else:
            way_to_open='w'
            
        if not metadata.is_empty():
            
            # open output file
            output_file = open(file_name, way_to_open)
            
            sentences, labels = metadata.get_metadata()
            for idx in range(len(sentences.get_sentences())):
                content_sentence = sentences.get_sentence(idx, False).encode('utf-8') 
                content_label = labels.get_labeled_sentence(idx, False).encode('utf-8') 
                
                output_file.write(str(offset + idx) + " " + \
                                  content_sentence + " s\n")
                output_file.write(str(offset + idx) + " " + \
                                  content_label + " l\n")
            # close output file
            output_file.close()
                    
class TextDataReader:

    def get_metadata_from_word_data(self, file_name):

        input_file = open(file_name, 'r')
        
        metadata = WordMetadata()

        sentence_label_pair = []
        for line in input_file:
            line = line.decode('utf-8')
            sentence_label_pair.append(line)
            if (len(sentence_label_pair) == 2):
                sentence, label = self.__pair_to_data(sentence_label_pair)
                if len(sentence) == 0 or len(label) == 0:
                    # on error
                    del sentence_label_pair[0]
                else:
                    metadata.add_metadata(sentence, label)
                    sentence_label_pair = []
        
        input_file.close()

        return metadata

    def __pair_to_data(self, pair):
        line_sentence = pair[0]
        line_label = pair[1]

        list_sentence = line_sentence.split()
        list_label = line_label.split()

        if list_sentence[0] != list_label[0] or list_sentence[-1] == list_label[-1]:
            # on error
            return [], []
        else:
            return list_sentence[1:-1], list_label[1:-1]

    def get_metadata_from_vector_data(self, file_name):
        
        input_file = open(file_name, 'r')

        metadata = VectorMetadata()
        
        sentence = []
        labeled_sentence = []

        for line in input_file:
            
            # sentence starts
            if line[0] == '#':
                if len(sentence) != 0 and len(labeled_sentence) != 0:
                    metadata.add_metadata(sentence, labeled_sentence)
                sentence = []
                labeled_sentence = []
            else:
                line_list = line.split()
                label = line_list[0].decode('utf-8')
                word_vectors = []
                for number in line_list[1:]:
                    word_vectors.append(float(number))
                    
                sentence.append(numpy.array(word_vectors, dtype=numpy.float32))
                labeled_sentence.append(label)

        # for the last sentence
        metadata.add_metadata(sentence, labeled_sentence)

        input_file.close()
        return metadata


class Tag:
    
    def __init__(self, tag_element):
        self.tag = tag_element.tag
        self.index = tag_element.get('start')
        self.start = int(self.index)
        self.end = int(tag_element.get('end'))
