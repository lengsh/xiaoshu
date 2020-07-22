#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
from loguru import logger
import time
import sqlite3
import bcrypt

logger.add(
    "log.log",
    retention="1 days",
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
)


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


class Bloge:
    """
    Define blog model-db object


    """

    def __init__(self, id, uId, title, contents):
        self.id = id
        self.uId = uId
        self.title = title
        self.contents = contents

    def __str__(self):
        return "{},{},{},{}".format(self.id, self.uId, self.title, self.contents)


def blog_db_init(db):
    """
Create db and tables;

before ......
    """
    try:
        c = db.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS
             author(Id INT PRIMARY KEY  NOT NULL, email text, nickname text, passwd text)"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS
             blog(Id int PRIMARY KEY  NOT NULL, title text, uId int, contents text)"""
        )
        c.execute("""CREATE INDEX index_author ON author(email)""")
        db.commit()
    except sqlite3.Error as e:
        print("Error, when db_init! {}".format(e.args[0]))
    finally:
        pass


def get_blog_by_id(db, id):
    blog = None
    cur = db.cursor()
    try:
        if int(id) > 0:
            cur.execute("SELECT Id, uId, title, contents FROM blog WHERE Id=?", (int(id),))
            ret = cur.fetchone()
            if len(ret) > 0:
                blog = Bloge(int(ret[0]), int(ret[1]), str(ret[2]), str(ret[3]))
    except Exception as e:
        logger.error(e.args[0])

    return blog


def get_blogs_by_page(db, page):
    blogs = None
    if page == None:
        page = 0
    else:
        page = int(page)
    sql = "SELECT Id, uId, title, contents FROM blog ORDER BY Id DESC LIMIT {},10".format(10*page)
    logger.debug(sql)
    cur = db.cursor()
    try:
        cur.execute(sql)
        rets = cur.fetchall()
        if len(rets) > 0:
            blogs = list()
            for r in rets:
                blogs.append(Bloge(int(r[0]), int(r[1]), str(r[2]), str(r[3])))
    except Exception as e:
        logger.error(e.args)
    return blogs

def post_new_blog(db, uid, title, contents):
    try:
        cur = db.cursor()
        cur.execute("SELECT Id FROM blog ORDER BY Id DESC LIMIT 1")
        r = cur.fetchone()
        logger.debug(r)
        if r == None :
            id = 1
        else:
            id = int( r[0]  ) + 1
        sql="INSERT INTO blog (Id,uId,title,contents) VALUES ({},{},{},{})".format(
                        id, uId, title, contents)
        logger.debug(sql)
        cur.execute(sql)
        db.commit()
    except Exception as e:
        logger.error(e)
        return False
    return True

def post_update_blog(db, id, title, contents):
    try:
        cur = db.cursor()
        sql ="UPDATE blog SET title = {}, contents = {} WHERE Id = {}".format(title, contents , int(id))
        logger.debug(sql)
        cur.execute(sql)
        db.commit()
    except Exception as e:
        logger.error(e)
        return False
    return True


def any_user_exists(db , email = ''):
    cur = db.cursor()
    sql = "SELECT Id FROM author LIMIT 1"
    if len(email) <= 4 :
        sql = "SELECT Id FROM author WHERE email='{}'".format(email)
    try:
        cur.execute(sql)
        usr = cur.fetchone()
    except Exception as e:
        logger.error(e.args)
        return False
    logger.debug("{} , result = {}".format(sql, usr))
    return bool(usr)    

def create_new_user(db, name, email, hash_password ):
    id = 0
    if any_user_exists(db, email) == False:
        logger.error("{} is exist, return error".format(email))
        return None
    try:
        cur = db.cursor()
        cur.execute("SELECT Id FROM author ORDER BY Id DESC LIMIT 1")
        if cur.fetchone() == None :
            id = 1
        else:
            id = int( cur.fetchone()[0]  ) + 1
        sql = "INSERT INTO author (Id, email, nickname, passwd) VALUES ({},{}, {}, {})".format(
            id, email, name, hashed_password)
        logger.debug(sql)    

        cur.execute("INSERT INTO author (Id, email, nickname, passwd) VALUES (?, ?, ?, ?)", (id, self.get_argument("email"), self.get_argument("name"), tornado.escape.to_unicode(hashed_password)))
        db.commit()
        return id
    except sqlite3.Error as e:
        logger.error(e.args[0])
        return None

def get_user_by_email(db, email):
    try:
        cur = db.cursor()
        sql = "SELECT Id,name, email, passwd FROM author WHERE email = '{}'".format(email) 
            
        logger.debug( sql )
        cur.execute( sql )
        author = cur.fetchone() 
    except sqlite3.Error as e:
        logger.error(e.args[0])
        return None
    if author == None or author[3] == None:
        return None
        
    user = Author( author[0], author[1], author[2], author[3] )
    return user
        

if __name__ == "__main__":
    dbname = os.path.join(os.path.dirname(__file__), "db", "example.db")
    db = sqlite3.connect(dbname)  #    'example.db')

    blog = get_blog_by_id(db, 1)
    print(blog)

    blogs = get_blogs_by_page(db, 0)
    for r in blogs:
        print(r)
