#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
from loguru import logger
import time
import sqlite3
import bcrypt
import asyncio
import dbmodel

'''
此处使用的sqlite3，应该不需要采用协程（异步支持）。
但，为了上层调用 mysql/postgresql (aiomysql/aiopg) 的异步能力保持一致的编码，所以这里也都给函数做了 rsync 标注。


'''

logger.add("log.log", rotation="1 days", colorize=True, format="<green>{time}</green> <level>{message}</level>", level="INFO")


async def blog_db_init(db):
    """
Create db and tables;

before ......
    """
    try:
        c = db.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS
             author(Id INTEGER PRIMARY KEY AUTOINCREMENT, email text, nickname text, passwd text)"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS
             blog(Id INTEGER PRIMARY KEY AUTOINCREMENT, title text, uId int, contents text)"""
        )
        c.execute("""CREATE INDEX index_author ON author(email)""")
        db.commit()
    except sqlite3.Error as e:
        print("Error, when db_init! {}".format(e.args[0]))
    finally:
        pass

async def get_blog_by_id(db, id):
    blog = None
    cur = db.cursor()
    try:
        if int(id) > 0:
            cur.execute('''SELECT blog.Id, blog.uId, blog.title, blog.contents, author.nickname 
            FROM blog, author WHERE blog.uId=author.Id AND blog.Id=?''', (int(id),))
            ret = cur.fetchone()
            if ret and len(ret) > 0:
                blog = dbmodel.Blog(int(ret[0]), int(ret[1]), str(ret[2]), str(ret[3]), str(ret[4]))
    except Exception as e:
        logger.error(e)

    return blog


async def get_blogs_by_page(db, page):
    blogs = list()
    if page == None:
        page = 0
    else:
        page = int(page)
    sql ='''SELECT blog.Id, blog.uId, blog.title, blog.contents, author.nickname FROM blog,author
        WHERE blog.uId=author.Id ORDER BY blog.Id DESC LIMIT {},10'''.format(10*page)
    logger.debug(sql)
    cur = db.cursor()
    try:
        cur.execute(sql)
        rets = cur.fetchall()
        if len(rets) > 0:
            for r in rets:
                blogs.append(dbmodel.Blog(int(r[0]), int(r[1]), str(r[2]), str(r[3]), str(r[4])))
    except Exception as e:
        logger.error(e.args)
    finally:
        return blogs

async def post_new_blog(db, uid, title, contents):
    try:
        cur = db.cursor()
        sql="INSERT INTO blog (uId,title,contents) VALUES ({},'{}','{}')".format(
                        uid, title, contents)
        logger.debug(sql)

        cur.execute("INSERT INTO blog (uId,title,contents) VALUES (?,?,?)",(
                        uid, title, contents,))
        db.commit()
    except Exception as e:
        logger.error(e)
        return False
    return True

async def post_update_blog(db, id, title, contents):
    try:
        cur = db.cursor()
        sql ="UPDATE blog SET title = '{}', contents = '{}' WHERE Id = {}".format(title, contents , int(id))
        logger.debug(sql)
        cur.execute("UPDATE blog SET title = ?, contents = ? WHERE Id = ?",(title, contents , int(id),))
        db.commit()
    except Exception as e:
        logger.error(e)
        return False
    return True


async def any_user_exists(db , email = ''):
    cur = db.cursor()
    sql = "SELECT Id FROM author LIMIT 1"
    if len(email) > 4 :
        sql = "SELECT Id FROM author WHERE email='{}'".format(email)
    try:
        cur.execute( sql )
        usr = cur.fetchone()
    except Exception as e:
        logger.error(e.args)
        return False
    logger.debug("{} , result = {}".format(sql, usr))
    return bool(usr)    

async def create_new_user(db, name, email, hash_password ):
    id = 0
    if any_user_exists(db, email) == True:
        logger.error("{} is exist, return error".format(email))
        return None
    try:
        cur = db.cursor()
        sql = "INSERT INTO author (email, nickname, passwd) VALUES ({}, {}, {})".format(
            email, name, hash_password)
        logger.debug(sql)    

        cur.execute("INSERT INTO author (email, nickname, passwd) VALUES (?, ?, ?)", (email,name,hash_password,))
        db.commit()
        return id
    except sqlite3.Error as e:
        logger.error(e.args[0])
        return None

async def get_user_by_email(db, email):
    try:
        cur = db.cursor()
        sql = "SELECT Id, nickname , email, passwd FROM author WHERE email = '{}'".format(email) 
            
        logger.debug( sql )
        cur.execute( sql )
        author = cur.fetchone() 
    except sqlite3.Error as e:
        logger.error(e.args[0])
        return None
    if author == None :
        return None
        
    user = Author( author[0], author[1], author[2], author[3] )
    return user

async def get_user_name_by_id(db, id):
    try:
        cur = db.cursor()
        sql = "SELECT nickname, email FROM author WHERE Id = '{}'".format(id) 
            
        logger.debug( sql )
        cur.execute( "SELECT nickname, email FROM author WHERE Id = ?",(id,)  )
        author = cur.fetchone() 
    except sqlite3.Error as e:
        logger.error(e.args[0])
        return None
    if author == None:
        return None
        
    return (author[0],author[1])

async def get_last_users(db, counts=10):
    try:
        users = list()
        cur = db.cursor()
        cur.execute( "SELECT Id, nickname, email FROM author ORDER BY Id DESC LIMIT 0,?",(counts,)  )
        rets = cur.fetchall()
        if len(rets) > 0:
            for r in rets:
                users.append( dbmodel.Author(int(r[0]), str(r[1]), str(r[2])))
    except sqlite3.Error as e:
        logger.error(e.args[0])
        return None
    return users

async def main():
    dbname = os.path.join(os.path.dirname(__file__), "example.db")
    db = sqlite3.connect(dbname)  #    'example.db')
    await blog_db_init(db)
    blog = await get_blog_by_id(db, 1)
    print(blog)

    blogs = await get_blogs_by_page(db, 0)
    if blogs:
        for r in blogs:
            print(r)

if __name__ == "__main__":
    # when python3 > 3.7
    asyncio.run(main())
    '''
    # when < python3.7
    loop = asyncio.get_event_loop()
    # Blocking call which returns when the hello_world() coroutine is done
    loop.run_until_complete( main())
    loop.close()
    '''
