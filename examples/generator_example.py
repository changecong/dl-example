#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Generator import Generator

generator = Generator('data-example/data-0')
tags = generator.get_all_tags([u'我', u'你', u'他', u'她', u'它', \
                               u'我们', u'你们', u'他们', u'她们', u'它们', \
                               'event', 'existentil', 'pleonastic', \
                               'generic', 'previous_utterance', 'other'])

metadata =  generator.label_sentences(generator.get_text(), tags)
sentences, labels = metadata.get_metadata()

print sentences.get_sentences()
print labels.get_labels()
