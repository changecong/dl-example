#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from Generator import Generator





if __name__ == '__main__':

    file_names = ['data-0', 'data-1']
    tags = [u'我', u'你', u'它', u'我们']


    for file in file_names:
        generator = Generator(file)
        
