#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Generator import XMLDataReader, TextDataReader

xmlreader = XMLDataReader('data-example/data-0')
tags = xmlreader.get_all_tags([u'我', u'你', u'他', u'她', u'它', \
                               u'我们', u'你们', u'他们', u'她们', u'它们', \
                               'event', 'existentil', 'pleonastic', \
                               'generic', 'previous_utterance', 'other'])

xml_metadata = xmlreader.label_sentences(xmlreader.get_text(), tags)

xmlreader.generate_text_file(xml_metadata, 'output')

textreader = TextDataReader('output')

text_metadata = textreader.get_metadata()

xml_sentences, xml_labels = xml_metadata.get_metadata()
text_sentences, text_labels = text_metadata.get_metadata()

print xml_sentences.get_sentences()
print text_sentences.get_sentences()
print xml_labels.get_labels()
print text_labels.get_labels()

