#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
from loguru import logger
#import time
import aiomysql
import asyncio
from dblib import dbmodel as dbmodel

logger.add("log.log", rotation="1 days", colorize=True, format="<green>{time}</green> <level>{message}</level>", level="INFO")

async def blog_db_init(db):
    """
Create db and tables;

before ......
    """
    try:
        async with db.cursor() as c:
            await c.execute(
                """CREATE TABLE IF NOT EXISTS
                author(Id INT PRIMARY KEY  NOT NULL, email text, nickname text, passwd text)"""
            )
            await c.execute(
                """CREATE TABLE IF NOT EXISTS
                blog(Id int PRIMARY KEY  NOT NULL, title text, uId int, contents text)"""
            )
            await c.execute("""CREATE INDEX index_author ON author(email(32))""")
            await db.commit()
        #await c.close()
    except Exception as e:
        logger.error(e)
    finally:
        pass

async def get_blog_by_id(db, id):
    blog = None
    try:
        async with db.cursor() as cur:
            if int(id) > 0:
                await cur.execute('''SELECT blog.Id, blog.uId, blog.title, blog.contents, author.nickname 
                    FROM blog, author WHERE blog.uId=author.Id AND blog.Id=%s''', (int(id)))
                ret = await cur.fetchone()
                if len(ret) > 0:
                    blog = dbmodel.Blog(int(ret[0]), int(ret[1]), str(ret[2]), str(ret[3]), str(ret[4]))
        #await cur.close()
    except Exception as e:
        logger.error(e)
    finally:
        pass
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
    try:
        async with db.cursor() as cur:
            await cur.execute(sql)
            rets = await cur.fetchall()
            if len(rets) > 0:
                for r in rets:
                    blogs.append(dbmodel.Blog(int(r[0]), int(r[1]), str(r[2]), str(r[3]), str(r[4])))
            #cur.close()
    except Exception as e:
        logger.error(e)
    finally:
        pass
    return blogs

async def post_new_blog(db, uid, title, contents):
    try:
        async with db.cursor() as cur:
            await cur.execute("SELECT Id FROM blog ORDER BY Id DESC LIMIT 1")
            r = await cur.fetchone()
            logger.debug(r)
            if r == None :
                id = 1
            else:
                id = int( r[0]  ) + 1
            sql="INSERT INTO blog (Id,uId,title,contents) VALUES ({},{},'{}','{}')".format(
                        id, uid, title, contents)
            logger.debug(sql)

            await cur.execute("INSERT INTO blog (Id,uId,title,contents) VALUES (%s,%s,%s,%s)",(
                        id, uid, title, contents,))
            await db.commit()
            #await cur.close()
    except Exception as e:
        logger.error(e)
        return False
    return True

async def post_update_blog(db, id, title, contents):
    try:
        async with db.cursor() as cur:
            sql ="UPDATE blog SET title = '{}', contents = '{}' WHERE Id = {}".format(title, contents , int(id))
            logger.debug(sql)
            await cur.execute("UPDATE blog SET title =%s, contents =%s WHERE Id = %s",(title, contents , int(id)))
            await db.commit()

    except Exception as e:
        logger.error(e)
        return False
    return True


async def any_user_exists(db , email = ''):
    sql = "SELECT Id FROM author LIMIT 1"
    if len(email) > 4 :
        sql = "SELECT Id FROM author WHERE email='{}'".format(email)
    try:
        async with db.cursor() as cur:
            await cur.execute( sql )
            usr = await cur.fetchone()

    except Exception as e:
        logger.error(e)
        return False
    logger.debug("{} , result = {}".format(sql, usr))
    return bool(usr)    

async def create_new_user(db, name, email, hash_password ):
    id = 0
    if await any_user_exists(db, email) == True:
        logger.error("{} is exist, return error".format(email))
        return None
    try:
        async with db.cursor() as cur:
            await cur.execute("SELECT Id FROM author ORDER BY Id DESC LIMIT 1")
            r = await cur.fetchone()
            if r == None :
                id = 1
            else:
                id = int( r[0] ) + 1
            sql = "INSERT INTO author (Id, email, nickname, passwd) VALUES ({},'{}', '{}', '{}')".format(
                id, email, name, hash_password)
            logger.debug(sql)    

            r = await cur.execute("INSERT INTO author (Id, email, nickname, passwd) VALUES (%s,%s,%s,%s)", (id, email,name,hash_password))
            logger.debug("insert author result = ", r)
        #await cur.close()
            await db.commit()
        return id
    except Exception as e:
        logger.error(e)
        return None

async def get_user_by_email(db, email):
    try:
        async with db.cursor() as cur:
            sql = "SELECT Id, nickname , email, passwd FROM author WHERE email = '{}'".format(email) 
            logger.debug( sql )

            await cur.execute( sql )
            author = await cur.fetchone() 
    except Exception as e:
        logger.error(e)
        return None
    if author == None :
        return None
        
    user = dbmodel.Author( author[0], author[1], author[2], author[3] )
    return user

async def get_user_name_by_id(db, id):
    try:
        async with db.cursor() as cur:
            sql = "SELECT nickname, email FROM author WHERE Id = {}".format(id) 
            
            logger.debug( sql )
            await cur.execute( "SELECT nickname, email FROM author WHERE Id = %s",(id)  )
            author = await cur.fetchone() 
    except Exception as e:
        logger.error(e)
        return None
    if author == None:
        return None  
    return (author[0],author[1])

async def get_last_users(db, counts=10):
    try:
        users = list()
        async with db.cursor() as cur:
            await cur.execute( "SELECT Id, nickname, email FROM author ORDER BY Id DESC LIMIT 0,%s",(counts)  )
            rets = await cur.fetchall()
            if len(rets) > 0:
                for r in rets:
                    users.append( dbmodel.Author(int(r[0]), str(r[1]), str(r[2])))
    except Exception as e:
        logger.error(e)
        return None
    return users

async def main():

    db = await aiomysql.connect(host='127.0.0.1', port=3306,
                                  user='root', password='', db='blog', charset='utf8mb4')

    await blog_db_init(db)
    await create_new_user(db, 'lengss','shushan@taobao.com','addfsfsfef33rfsdcdsf')
    db.close()


if __name__ == "__main__":
    '''    
    loop = asyncio.get_event_loop()
    loop.run_until_complete( main())
    loop.close()
    '''
# python3.7+
    asyncio.run(main())
