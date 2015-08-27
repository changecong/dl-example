#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Generator import Generator

generator = Generator('data/data-0')
tags = generator.get_all_tags([u'我', 'event'])

metadata =  generator.label_sentences(generator.get_text(), tags)
sentences, labels = metadata.get_metadata()

print sentences.get_sentences()
print labels.get_labels()
