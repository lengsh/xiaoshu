#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.template as template
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.locks
import tornado.web
from  loguru import logger
import time
from tornado import gen
import tornado.httpclient
import sqlite3
import bcrypt

from tornado.options import  options,define 
define("port",default=8080,help="on the given help", type="int")
logger.add("log.log", retention="1 days", colorize=True, format="<green>{time}</green> <level>{message}</level>")

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        cookies =  self.get_secure_cookie("blog_user")
        logger.debug("blog_user cookie = {}".format( cookies ))
        if cookies == None :
            return None
        ret = str(cookies).split("|", 1)
        logger.debug("current user = {}".format(ret))
        if len(ret)>= 2:
            self.current_user = ret[1]
            logger.debug("current user = {}".format(ret[1]))
            return self.current_user
        
    async def any_author_exists(self ):
        cur = self.application.db.cursor()
        cur.execute("SELECT * FROM author LIMIT 1")
        usr = cur.fetchone()
        logger.debug("slect * from author , result = {}".format(usr))
        return bool(usr)


class IndexHandler(BaseHandler):
     def get(self):
        students = [dict(name='david'), dict(name='jack')]
        self.render('base.html',students=students, user=self.current_user )

class HelpPageHandler(BaseHandler):
     @tornado.web.authenticated
     def get(self):
        students = [dict(name='lengsh'), dict(name='mark')]
        self.render('bold.html',students=students)

class SlowPageHandler(tornado.web.RequestHandler):
     def get(self):
        self.write("hello, Mr. Slow !")

class InbPageHandler(BaseHandler):
     @tornado.web.authenticated
     def get(self):
        students = [dict(name='lengsh'), dict(name='mark')]
        self.render('inb.html',students=students)

class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!</h1>'

class UserModule(tornado.web.UIModule):
    def render(self):
        if self.current_user :
            return '{}'.format(self.current_user)
        else:
            return 'Anonymouse'

class AuthCreateHandler(BaseHandler):
    def get(self):
        self.render("create_author.html")

    async def post(self):
        #if await self.any_author_exists():
        #    raise tornado.web.HTTPError(400, "author already created")
        hashed_password = await tornado.ioloop.IOLoop.current().run_in_executor(
            None,
            bcrypt.hashpw,
            tornado.escape.utf8(self.get_argument("password")),
            bcrypt.gensalt(),
        )
        id = 0
        try:
            cur = self.application.db.cursor()
            cur.execute("SELECT Id FROM author order by Id desc limit 1")
            if cur.fetchone() == None :
                id = 1
            else:
                id = int( cur.fetchone()[0]  ) + 1
            sql = "INSERT INTO author (Id, email, nickname, passwd) values ({},{}, {}, {})".format(id, self.get_argument("email"),
                self.get_argument("name"),
                tornado.escape.to_unicode(hashed_password))
            logger.debug(sql)    

            cur.execute("INSERT INTO author (Id, email, nickname, passwd) values (?, ?, ?, ?)", (id, self.get_argument("email"), self.get_argument("name"), tornado.escape.to_unicode(hashed_password)))

            self.application.db.commit()
        except sqlite3.Error as e:
            logger.error(e.args[0])
        finally:
            pass

        logger.debug("{}".format(id))
        # self.set_secure_cookie("blog_user", str(id))
        self.set_secure_cookie("blog_user", "{}|{}".format(str(id), self.get_argument("name")) )
        self.redirect(self.get_argument("next", "/"))

class AuthLoginHandler(BaseHandler):
    async def get(self):
        # If there are no authors, redirect to the account creation page.
        if not await self.any_author_exists():
            self.redirect("/auth/create")
        else:
            self.render("login.html", error=None)

    async def post(self):
        try:
            cur = self.application.db.cursor()
            sql = "SELECT * FROM author WHERE email = '{}'".format(self.get_argument("email")) 
            
            logger.debug( sql )
            cur.execute( sql )
            author = cur.fetchone() 
            logger.debug( author )
        except sqlite3.Error as e:
            logger.error(e.args[0])
            self.render("login.html", error="email not found ")
            return
        if author == None or author[3] == None:
            self.render("login.html", error="no such user")
            return
        password_equal = await tornado.ioloop.IOLoop.current().run_in_executor(
            None,
            bcrypt.checkpw,
            tornado.escape.utf8(self.get_argument("password")),
            tornado.escape.utf8(author[3]),
        )
        if password_equal:
            self.set_secure_cookie("blog_user", "{}|{}".format(str(author[0]), author[2]) )
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("login.html", error="incorrect password")

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("blog_user")
        self.redirect(self.get_argument("next", "/"))


def db_init(db ):
# Create table
    try:
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS
             author(Id INT PRIMARY KEY  NOT NULL, email text, nickname text, passwd text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS
             blog(Id int PRIMARY KEY  NOT NULL, title text, uId int, contents text)''')
        c.execute('''CREATE INDEX index_author ON author(email)''')
        db.commit()
    except sqlite3.Error as e:
        print("Error, when db_init! {}".format(e.args[0]))
    finally:
        pass

class Application(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        handlers = [
                    (r'/', IndexHandler), 
                    (r'/bold',HelpPageHandler), 
                    (r'/inb',InbPageHandler),
                    (r"/auth/create", AuthCreateHandler),
                    (r"/auth/login", AuthLoginHandler),
                    (r"/auth/logout", AuthLogoutHandler)
        ]

        settings = dict(
            blog_title=u"Tornado Blog",
            template_path=os.path.join(os.path.dirname(__file__), "html"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={'Hello': HelloModule, 'UserName':UserModule},
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)



async def main():
    tornado.options.parse_command_line()
    # Create the global db connection .
    db = sqlite3.connect('example.db')
    db_init(db)
    app = Application(db)
    app.listen(options.port)
        # In this demo the server will simply run until interrupted
        # with Ctrl-C, but if you want to shut down more gracefully,
        # call shutdown_event.set().
    shutdown_event = tornado.locks.Event()
    await shutdown_event.wait()
    print("shutdown -h now")
    shutdown_event.set()

if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)
    print("Exit...")
