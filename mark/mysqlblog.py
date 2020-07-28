#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
from loguru import logger
#import time
import aiomysql
import asyncio
import dbmodel 

logger.add("logs/log.log", rotation="1 days", colorize=True, format="<green>{time}</green> <level>{message}</level>", level="INFO")

async def blog_db_init(db):
    """
Create db and tables;

before ......
    """
    try:
        async with db.cursor() as c:
            await c.execute(
                """CREATE TABLE IF NOT EXISTS author(Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, email varchar(128) NOT NULL unique, nickname varchar(256), passwd varchar(128))"""
            )
            await c.execute( """CREATE TABLE IF NOT EXISTS
                blog(Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, title text, uId int, contents text, 
                utime float default 0.0, mtime TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP)"""
            )
            await c.execute("""CREATE INDEX index_author ON author(email(32))""")
            await c.execute( """CREATE TABLE IF NOT EXISTS question(Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, topic varchar(256), level int, result int, priority int)"""
            )
            ##########################
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
                    blog = dbmodel.Blog(int(ret[0]), int(ret[1]), str(ret[2]), str(ret[3]),0,0, str(ret[4]))
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
    sql ='''SELECT blog.Id, blog.uId, blog.title, blog.contents, blog.utime, blog.mtime, author.nickname FROM blog,author
        WHERE blog.uId=author.Id ORDER BY blog.Id DESC LIMIT {},10'''.format(10*page)
    logger.debug(sql)
    try:
        async with db.cursor() as cur:
            await cur.execute(sql)
            rets = await cur.fetchall()
            if len(rets) > 0:
                for r in rets:
                    blogs.append(dbmodel.Blog(int(r[0]), int(r[1]), str(r[2]), str(r[3]), r[4] , r[5], str(r[6])))
            #cur.close()
    except Exception as e:
        logger.error(e)
    finally:
        pass
    return blogs

async def post_new_blog(db, uid, title, contents, utime=0.0):
    try:
        async with db.cursor() as cur:
            sql="INSERT INTO blog (uId,title,contents,utime) VALUES ({},'{}','{}',{})".format(
                        uid, title, contents, utime)
            logger.debug(sql)

            await cur.execute("INSERT INTO blog (uId,title,contents,utime) VALUES (%s,%s,%s,%s)",(
                        uid, title, contents, utime))
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
            sql = "INSERT INTO author (email, nickname, passwd) VALUES ('{}', '{}', '{}')".format(
                email, name, hash_password)
            logger.debug(sql)    

            r = await cur.execute("INSERT INTO author (email, nickname, passwd) VALUES (%s,%s,%s)", (email,name,hash_password))
            logger.debug("insert author result = ", r)
        #await cur.close()
            await db.commit()
            await cur.execute("SELECT Id, nickname, email FROM author WHERE email = %s", email) 
            author = await cur.fetchone() 
            return author[0]

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

#############################################
async def get_random_questions(db, ids):
    questions = list()
    instr = '('
    for id in ids :
        instr +="'{}',".format(id)
    instr +='-1)'
    sql ='''SELECT question.Id, question.topic, question.result FROM question
        WHERE question.Id in {}'''.format(instr)
    logger.debug(sql)
    try:
        async with db.cursor() as cur:
            await cur.execute(sql)
            rets = await cur.fetchall()
            if len(rets) > 0:
                for r in rets:
                    questions.append(dbmodel.Question(int(r[0]), str(r[1]), int(r[2]) ))
            #cur.close()
    except Exception as e:
        logger.error(e)
    finally:
        pass
    return questions


async def get_answer_best_top(db, counts=10):
    blogs = list()
    sql ='''SELECT blog.Id, blog.uId, blog.title, blog.utime, blog.mtime, author.nickname FROM blog,author
        WHERE blog.uId=author.Id and blog.utime > 0 ORDER BY blog.utime DESC LIMIT {}'''.format(counts)
    logger.debug(sql)
    try:
        async with db.cursor() as cur:
            await cur.execute(sql)
            rets = await cur.fetchall()
            if len(rets) > 0:
                for r in rets:
                    blogs.append(dbmodel.Blog(int(r[0]), int(r[1]), str(r[2]), '', r[3] , r[4], str(r[5])))
            #cur.close()
    except Exception as e:
        logger.error(e)
    finally:
        pass
    return blogs

#####################
async def question_db_init(db):
    imax = 99
    jmax = 99
    total = 0
    cur = await db.cursor()
    for i in range(100):
        for j in range(100):
            if i==0 or j==0:
                continue
            re1 = i + j
            s1 = "{} + {}".format(i,j)
            sql1 = "insert into question(topic, level, result, priority) values ('{}',{},{},{})".format(s1, 1, re1, 1)
            print(sql1)
            await cur.execute(sql1)
            await db.commit()
            total += 1
            re2 = i - j
            s2 = "{} - {}".format(i,j)
            if re2 > 0:
                sql2 = "insert into question(topic, level, result, priority) values ('{}',{},{},{})".format(s2, 1, re2, 1)
                print(sql2)
                await cur.execute(sql2)
                await db.commit()
                total += 1
    print("TOTAL = ", total)
    await cur.close()

iTOTAL = 14652

def get_random_array( counts=10, MAXID = iTOTAL):
    import random
    ar = list()
    for i in range(counts):
        ar.append( random.randint(1, MAXID) )
    return ar


async def main():
    db = await aiomysql.connect(host='127.0.0.1', port=3306,
                                  user='root', password='', db='blog', charset='utf8mb4')
    await blog_db_init(db)
    await question_db_init(db)
    aID = get_random_array(10) 
    rs = await get_random_questions(db, aID )
    for r in rs:
        print(r)
    idlist = ','.join(map(str,aID))
    db.close()
    print(idlist)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete( main())
    loop.close()
# python3.7+
#    asyncio.run(main())
