#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Author:
    """
    Define user object

    """

    def __init__(self, id, name, email, upasswd = ''):
        self.id = id
        self.name = name
        self.email = email
        self.upasswd = upasswd

    def __str__(self):
        return "{},{},{},{}".format(self.id, self.name, self.email, self.upasswd)

class Blog:
    """
    Define blog model-db object


    """

    def __init__(self, id, uId, title, contents, utime=0, mtime=0, uname=''):
        self.id = id
        self.uId = uId
        self.title = title
        self.contents = contents
        self.utime = utime
        self.author = uname
        self.mtime = mtime

    def __str__(self):
        return "{},{},{},{},{},{}".format(self.id, self.uId, self.title, self.contents, self.utime, self.mtime)

def Blog_to_json(obj):
    return {
        "id": obj.id,
        "uId": obj.uId,
        "title": obj.title,
        "contents": obj.contents,
        "utime":obj.utime,
        "mtime":obj.mtime,
        "author": obj.author
    }

def Blog_from_json(d):
    return  Bloge( d["id"], d["uId"], d["title"], d["contents"], d["utime"], d["mtime"], d["author"])


class Question:
    """
    Define Question model-db object

    id, topic, level, result , priority
    """

    def __init__(self, id, topic, result, in_result=0):
        self.id = id
        self.topic = topic
        self.result = result
        self.in_result = in_result

    def __str__(self):
        return "{},{},{},{}".format(self.id, self.topic, self.result, self.in_result)

if __name__ == "__main__":
    print("hello,world!")
    
