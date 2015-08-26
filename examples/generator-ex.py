#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Generator import Generator

generator = Generator('../data/Wang_Final/CHT_CMN_20120817.0001.su.xml')
tags = generator.get_all_tags([u'我', 'event'])
print tags
