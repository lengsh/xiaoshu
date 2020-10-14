#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path

# import time
import aiomysql
import asyncio
import dbmodel
import logging

logger = logging.getLogger(__name__)

async def patent_db_init(db):
    """
Create db and tables;

before ......
    """
    try:
        async with db.cursor() as c:
            await c.execute("""CREATE TABLE IF NOT EXISTS wordomit(Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, word varchar(64) NOT NULL unique) """)
            await c.execute("""CREATE TABLE IF NOT EXISTS phraseomit(Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, phrase varchar(256) NOT NULL unique) """)
            await c.execute("""CREATE TABLE IF NOT EXISTS phrasedict(Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, phrase varchar(256) NOT NULL unique, descr text) """)
            await c.execute("""CREATE TABLE IF NOT EXISTS document(Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, filename varchar(128) NOT NULL unique, descr text) """)
            await c.execute("""CREATE TABLE IF NOT EXISTS
                keywords(Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, docId int, word varchar(64), counts int, mtime TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6) )""")
            # Mysql不同版本，有不同的函数定义：CURRENT_TIMESTAMP  or CURRENT_TIMESTAMP（6）
            await c.execute( """CREATE TABLE IF NOT EXISTS phrases(Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, phrase varchar(256), counts int, docId int)""")
            await c.execute("""CREATE unique INDEX idx_keywords ON keywords(docId, word) """)
            await c.execute("""CREATE unique INDEX idx_phrase ON phrases(docId, phrase) """)
            ##########################
            await db.commit()
        # await c.close()
    except Exception as e:
        print(e)
    finally:
        pass


async def get_keywords_by_docId(db, docid):
    words = list() 
    try:
        async with db.cursor() as cur:
            if int(docid) > 0:
                await cur.execute(
                    """SELECT Id, word, counts, docId FROM keywords WHERE docId=%s ORDER BY counts DESC """,
                    (int(docid)),
                )
                rets = await cur.fetchall()
                if len(rets) > 0:
                    for r in rets:
                        words.append(dbmodel.Word( int(r[0]), str(r[1]), int(r[2]), int(r[3]),))
    except Exception as e:
        logger.error(e)
    finally:
        pass
    return words 


async def get_phrases_by_docId(db, docid):
    phrases = list() 
    try:
        async with db.cursor() as cur:
            if int(docid) > 0:
                await cur.execute(
                    """SELECT Id, phrase, counts, docId FROM phrases WHERE docId=%s ORDER BY counts DESC""",
                    (int(docid)),
                )
                rets = await cur.fetchall()
                if len(rets) > 0:
                    for r in rets:
                        phrases.append(dbmodel.Phrase( int(r[0]), str(r[1]), int(r[2]), int(r[3]),))
    except Exception as e:
        logger.error(e)
    finally:
        pass
    return phrases 


async def add_omit_word(db, word):
    try:
        async with db.cursor() as cur:
            await cur.execute("INSERT INTO wordomit(word) VALUES (%s)", (word),)
            await db.commit()
    except Exception as e:
        logger.error(e)
        return False
    return True


async def delete_omit_word(db, id):
    try:
        async with db.cursor() as cur:
            await cur.execute( "DELETE FROM wordomit WHERE Id = %s", (int(id)),)
            await db.commit()

    except Exception as e:
        logger.error(e)
        return False
    return True

async def get_all_omit_words(db, counts=2000):
    try:
        ret = list()
        async with db.cursor() as cur:
            await cur.execute(
                "SELECT Id, word FROM wordomit LIMIT 0,%s",
                (counts),
            )
            rets = await cur.fetchall()
            if len(rets) > 0:
                for r in rets:
                    ret.append(dbmodel.Word(int(r[0]), str(r[1])))
    except Exception as e:
        logger.error(e)
        return None
    return ret


async def add_omit_phrase(db, word):
    try:
        async with db.cursor() as cur:
            await cur.execute("INSERT INTO phraseomit(phrase) VALUES (%s)", (word),)
            await db.commit()
    except Exception as e:
        logger.error(e)
        return False
    return True


async def delete_omit_phrase(db, id):
    try:
        async with db.cursor() as cur:
            await cur.execute( "DELETE FROM phraseomit WHERE Id = %s", (int(id)),)
            await db.commit()

    except Exception as e:
        logger.error(e)
        return False
    return True

async def get_all_omit_phrases(db, counts=2000):
    try:
        ret = list()
        async with db.cursor() as cur:
            await cur.execute(
                "SELECT Id, phrase FROM phraseomit LIMIT 0,%s",
                (counts),
            )
            rets = await cur.fetchall()
            if len(rets) > 0:
                for r in rets:
                    ret.append(dbmodel.Phrase(int(r[0]), str(r[1])))
    except Exception as e:
        logger.error(e)
        return None
    return ret

async def add_document(db, fname):
    try:
        async with db.cursor() as cur:
            await cur.execute("INSERT INTO document(filename) VALUES (%s)", (fname),)
            await db.commit()
            await cur.execute("SELECT Id FROM document WHERE filename=%s", (fname),)
            doc = await cur.fetchone()
            if len(doc) > 0 :
                return int(doc[0])
    except Exception as e:
        logger.error(e)
    return -1

async def delete_document(db, id):
    try:
        async with db.cursor() as cur:
            await cur.execute( "DELETE FROM phrases WHERE docId = %s", (int(id)),)
            await cur.execute( "DELETE FROM keywords WHERE docId = %s", (int(id)),)
            await cur.execute( "DELETE FROM document WHERE Id = %s", (int(id)),)
            await db.commit()
    except Exception as e:
        logger.error(e)
        return False
    return True

async def get_all_documents(db, fro=0, counts=100):
    try:
        ret = list()
        async with db.cursor() as cur:
            await cur.execute(
                "SELECT Id, filename, descr FROM document LIMIT %s,%s",
                (fro, counts),
            )
            rets = await cur.fetchall()
            if len(rets) > 0:
                page = int(fro/counts)
                for r in rets:
                    ret.append(dbmodel.Document(int(r[0]), str(r[1]), str(r[2]), page))
    except Exception as e:
        logger.error(e)
        return None
    return ret

async def add_doc_word(db, docId, word, counts):
    try:
        async with db.cursor() as cur:
            await cur.execute(
                "INSERT INTO keywords(docId, word, counts) VALUES (%s,%s,%s)",
                (int(docId), word, int(counts)),
            )
            await db.commit()
    except Exception as e:
        logger.error(e)
        return False
    return True


async def delete_doc_word(db, id):
    try:
        async with db.cursor() as cur:
            await cur.execute(
                "DELETE FROM keywords WHERE Id = %s",
                (int(id)),
            )
            await db.commit()

    except Exception as e:
        logger.error(e)
        return False
    return True

async def add_doc_phrase(db, docId, phrase, counts):
    try:
        async with db.cursor() as cur:
            await cur.execute(
                "INSERT INTO phrases(docId, phrase, counts) VALUES (%s,%s,%s)",
                (int(docId), phrase, int(counts)),
            )
            await db.commit()
    except Exception as e:
        logger.error(e)
        return False
    return True


async def delete_doc_phrase(db, id):
    try:
        async with db.cursor() as cur:
            await cur.execute(
                "DELETE FROM phrases WHERE Id = %s",
                (int(id)),
            )
            await db.commit()

    except Exception as e:
        logger.error(e)
        return False
    return True


async def omit_word_db_init(db):
    omit_word_list = ['a','an','the','is','am','are','of','at','on','in','also','else','to','be','for','or','by','and','as']
    omit_phrase_list = ['is a','by the','in a','in the','of the','to a','and the','for an']
    sql = "INSERT INTO wordomit(word) values ('a'),('an'),('the'),('is'),('am'),('are'),('of'),('at');"
    try:
        async with db.cursor() as c:
            await c.execute(sql)
            await db.commit()
        # await c.close()
    except Exception as e:
        logger.error(e)
    finally:
        pass


async def omit_phrase_db_init(db):
    sql = "INSERT INTO phraseomit(phrase) values ('is a'),('by the'),('to a'),('and the');"
    try:
        async with db.cursor() as c:
            await c.execute(sql)
            await db.commit()
        # await c.close()
    except Exception as e:
        logger.error(e)
    finally:
        pass

async def main():
    db = await aiomysql.connect(
        host="127.0.0.1",
        port=3306,
        user="lengsh",
        password="123456",
        db="patent",
        charset="utf8mb4",
    )

#    await patent_db_init(db)
#    await omit_word_db_init(db)
#    await omit_phrase_db_init(db)

    rs = await get_all_omit_words(db)
    for r in rs:
        print(r)
    rs = await get_all_omit_phrases(db)
    for r in rs:
        print(r)
    db.close()


if __name__ == "__main__":
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(main())
#    loop.close()
# python3.7+
    asyncio.run(main())
