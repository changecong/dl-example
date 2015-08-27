#!/usr/bin/env python
# -*- coding: utf-8 -*-        

from lxml import etree
from WordMetadata import WordMetadata

import xml.etree.ElementTree as ET


class Generator:

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

        for i in range(1, len(sentences_and_positions) - 1):
            temp_sentence = sentences_and_positions[i]
            if isinstance(temp_sentence, basestring) and len(temp_sentence) != 0:

                temp_words = temp_sentence.split()
                temp_labels = ['NA'] * len(temp_words)

                index = temp_sentence.find(magic_word)
                count = 0
                label_index = 0
                while index != -1:
                    lable = ""
                    if tags.get(str(index + 1), False):
                        label = tags[str(index + 1)].tag
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

class Tag:
    
    def __init__(self, tag_element):
        self.tag = tag_element.tag
        self.index = tag_element.get('start')
        self.start = int(self.index)
        self.end = int(tag_element.get('end'))
