#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class KwWord:
    """
    Define user object

    """

    def __init__(self, id, word, descr='', counts=0, docId=-1):
        self.id = id
        self.word = word
        self.descr = descr
        self.counts = counts
        self.docId = docId
    def __str__(self):
        return "{},{},{},{},{}".format(self.id, self.word, self.descr, self.counts, self.docId)

class Word:
    """
    Define user object

    """

    def __init__(self, id, word, counts=0, docId=-1):
        self.id = id
        self.word = word
        self.counts = counts
        self.docId = docId

    def __str__(self):
        return "{},{},{},{}".format(self.id, self.word, self.counts, self.docId)

class Phrase:
    """
    Define blog model-db object


    """

    def __init__(self, id, phrase, counts=0, docId=-1):
        self.id = id
        self.phrase = phrase 
        self.counts = counts
        self.docId = docId

    def __str__(self):
        return "{},{},{},{}".format(self.id, self.phrase, self.counts, self.docId)


class Document:
    """
    Define document model-db object


    """

    def __init__(self, id, docName, descr = '', page=0):
        self.id = id
        self.docName = docName
        self.descr = descr
        self.page = page

    def __str__(self):
        return "{},{},{}".format(self.id, self.docName, self.descr)


if __name__ == "__main__":
    print("hello,world!")
    
