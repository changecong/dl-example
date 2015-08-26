#!/usr/bin/env python                                                                                                                                                                                            
# -*- coding: utf-8 -*-        

from lxml import etree
import xml.etree.ElementTree as ET

class Generator:

    def __init__(self, file_name):
        self.__tree = etree.parse(file_name)
        self.__root = self.__tree.getroot()
        self.__tags_element = self.__root.findall('TAGS')[0]

    def __get_tags_by_name(self, tag_name):

        # get all tag whose name is <tag_name>
        tags = self.__tags_element.findall(tag_name)
 
        tags_dict = {}
        for tag in tags:
            temp_tag = Tag(tag)
            tags_dict[temp_tag.index] = temp_tag

        return tags_dict

    def get_all_tags(self, tag_list):
        
        all_tags = {}

        for tag in tag_list:
            tags_dict = self.__get_tags_by_name(tag)
            all_tags.update(tags_dict)

        return all_tags
            

class Tag:
    
    def __init__(self, tag_element):
        self.tag = tag_element.tag
        self.index = tag_element.get('start')
        self.start = int(self.index)
        self.end = int(tag_element.get('end'))
