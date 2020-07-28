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

    def __init__(self, id, uId, title, contents, uname=''):
        self.id = id
        self.uId = uId
        self.title = title
        self.contents = contents
        self.author = uname

    def __str__(self):
        return "{},{},{},{}".format(self.id, self.uId, self.title, self.contents)

def Blog_to_json(obj):
    return {
        "id": obj.id,
        "uId": obj.uId,
        "title": obj.title,
        "contents": obj.contents,
        "author": obj.author
    }

def Blog_from_json(d):
    return  Bloge( d["id"], d["uId"], d["title"], d["contents"], d["author"])


if __name__ == "__main__":
    print("hello,world!")
    
