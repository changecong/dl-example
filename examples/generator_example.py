#!/usr/bin/env python
# -*- coding: utf-8 -*-

from generator import XMLDataReader, TextDataReader

xmlreader = XMLDataReader('data-example/data-0')
tags = xmlreader.get_all_tags([u'我', u'你', u'他', u'她', u'它', \
                              u'我们', u'你们', u'他们', u'她们', u'它们', \
                              'event', 'existentil', 'pleonastic', \
                              'generic', 'previous_utterance', 'other'])

xml_metadata = xmlreader.label_sentences(xmlreader.get_text(), tags)

xmlreader.generate_text_file(xml_metadata, 'labeled_words')

xml_sentences, xml_labels = xml_metadata.get_metadata()

print xml_sentences.get_sentences()
print xml_labels.get_labels()

