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
import bloger
import signal

from tornado.options import  options,define 
define("port",default=8080,help="on the given help", type="int")
logger.add("log.log", retention="1 days", colorize=True, format="<green>{time}</green> <level>{message}</level>")

class BaseHandler(tornado.web.RequestHandler):
    async def prepare(self):
         # get_current_user cannot be a coroutine, so set
         # self.current_user in prepare instead.
        cookies =  self.get_secure_cookie("blog_user")
        logger.debug("blog_user cookie = {}".format( cookies ))
        if cookies == None :
            return
        rets = str(cookies, encoding="utf8")
        logger.debug(rets)
        ret = rets.split("|", 1)
        logger.debug("current user = {}".format(ret))
        if len(ret)>= 2:
            user = bloger.Author(int(ret[0]), str(ret[1]),'')
            self.current_user = user
            
    '''            
    def get_current_user(self):
        cookies =  self.get_secure_cookie("blog_user")
        logger.debug("blog_user cookie = {}".format( cookies ))
        if cookies == None :
            return None
        rets = str(cookies, encoding="utf8")
        logger.debug(rets)
        ret = rets.split("|", 1)
        logger.debug("current user = {}".format(ret))
        if len(ret)>= 2:
            user = bloger.Author(int(ret[0]), str(ret[1]),'')
            self.current_user = user
            logger.debug("current user id={}, name={}".format(ret[0], ret[1]))
            return self.current_user
    '''
    async def any_author_exists(self ):
        return bloger.any_user_exists( self.application.db )

class IndexHandler(BaseHandler):
     def get(self):
        students = [dict(name='david'), dict(name='jack')]
        self.render('base.html',students=students, user=self.current_user )
                
class BlogPostHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self):
        id = self.get_argument("id", None)
        blog = None
        if id:
            blog = bloger.get_blog_by_id( self.application.db, int(id))
        self.render("post.html", blog= blog)

    @tornado.web.authenticated
    async def post(self):
        contents = self.get_argument("contents", None)
        id = self.get_argument("id", None)
        title = self.get_argument("title", None)
        # update 
        if id:
                # update 
            bloger.post_update_blog(self.application.db, id, title, contents)    
        else:
                # insert
            bloger.post_new_blog(self.application.db, self.current_user.id, title, contents)
        self.redirect("/blog/read")

class BlogReadHandler(BaseHandler):
     @tornado.web.authenticated
     async def get(self):
        blogs = None
        id = self.get_argument("id", None) 
        page = self.get_argument("page", None) 
        if id != None :
            blog = bloger.get_blog_by_id(self.application.db, int(id))
            if blog :
                blogs = list()
                blogs.append(blog)
        else :
            if page == None:
                page = 0
            blogs = bloger.get_blogs_by_page( self.application.db, int(page) )
        
        self.render("read.html", blogs = blogs )



class LoginModule(tornado.web.UIModule):
    def render(self):
        if self.current_user :
            return '<a href="/auth/logout">Logout</a>'
        else:
            return '<a href="/auth/login">Login</a> | <a href="/auth/create">Regist</a>'

class UserModule(tornado.web.UIModule):
    def render(self):
        if self.current_user :
            logger.debug("{},{}".format(self.current_user.id, self.current_user.name))
            return '{}'.format(self.current_user.name)
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
       
        email = self.get_argument("email", None)
        name = self.get_argument("name", None)
        uni_hash_passwd = tornado.escape.to_unicode(hashed_password)
        id = bloger.create_new_user(self.application.db, name, email, uni_hash_passwd)
        if id :
            self.set_secure_cookie("blog_user", "{}|{}".format(str(id), name) )

        self.redirect(self.get_argument("next", "/"))

class AuthLoginHandler(BaseHandler):
    async def get(self):
        # If there are no authors, redirect to the account creation page.
        if not await self.any_author_exists():
            self.redirect("/auth/create")
        else:
            self.render("login.html", error=None)

    async def post(self):
        email = self.get_argument("email", None)
        user = bloger.get_user_by_email(self.application.db, email)
        if user == None:
            self.render("login.html", error="no such user ")
            return
        password_equal = await tornado.ioloop.IOLoop.current().run_in_executor(
            None,
            bcrypt.checkpw,
            tornado.escape.utf8(self.get_argument("password")),
            tornado.escape.utf8( user.upasswd ),
        )
        if password_equal:
            self.set_secure_cookie("blog_user", "{}|{}".format(str(user.id),  user.name ) )
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("login.html", error="incorrect password")

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("blog_user")
        self.redirect(self.get_argument("next", "/"))


class Application(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        handlers = [
                    (r'/', IndexHandler), 
                    (r'/blog/post',BlogPostHandler), 
                    (r'/blog/read',BlogReadHandler),
                    (r"/auth/create", AuthCreateHandler),
                    (r"/auth/login", AuthLoginHandler),
                    (r"/auth/logout", AuthLogoutHandler)
        ]

        settings = dict(
            blog_title=u"Tornado Blog",
            template_path=os.path.join(os.path.dirname(__file__), "html"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={'LogInOut': LoginModule, 'UserName':UserModule},
            xsrf_cookies=True,
            cookie_secret="__TODO:_YOUR_OWN_RANDOM_VALUE_HERE__ABCDEFG.......",
            login_url="/auth/login",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)

async def main():
    tornado.options.parse_command_line()
    # Create the global db connection .
    dbname = os.path.join(os.path.dirname(__file__), "db", "example.db")

    db = sqlite3.connect( dbname)  #    'example.db')
    bloger.blog_db_init(db)
    app = Application(db)
    app.listen(options.port)
        # In this demo the server will simply run until interrupted
        # with Ctrl-C, but if you want to shut down more gracefully,
        # call shutdown_event.set().
    shutdown_event = tornado.locks.Event()
    def shutdown( signum, frame ):

        logger.error("graceful shutdown?!!!! signum={}".format(signum))
        logger.error("clear all memery and  shutdown  database !!!!")
        db.close()
        shutdown_event.set()


    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    await shutdown_event.wait()
    print("\n\nshutdown -h now\n\n")

if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)

