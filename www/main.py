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
import signal
import json
import dblib.sqliteblog as myblog
#import dblib.mysqlblog as myblog
#import dblib.postgreblog as myblog
import logging

from tornado.options import  options,define 
define("port",default=8080,help="server listen port", type=int)
define("dbinit",default=0,help="if need to init db, 0:No; 1:Yes", type=int)

logger.add("log.log", rotation="1 days", colorize=True, format="<green>{time}</green> <level>{message}</level>", level="INFO")


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
            user = myblog.Author(int(ret[0]), str(ret[1]),'')
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
            user = myblog.Author(int(ret[0]), str(ret[1]),'')
            self.current_user = user
            logger.debug("current user id={}, name={}".format(ret[0], ret[1]))
            return self.current_user
    '''
    async def any_author_exists(self ):
        return await myblog.any_user_exists( self.application.db )

class IndexHandler(BaseHandler):
    async def get(self):
        users = await myblog.get_last_users( self.application.db )
        students = [dict(name='david'), dict(name='jack')]
        self.render('base.html',students=students, users=users )


class ServiceHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self):
        blogs = list()
        id = self.get_argument("id", None) 
        page = self.get_argument("page", None) 
        if id != None :
            blog = await myblog.get_blog_by_id(self.application.db, int(id))
            if blog :
                blogs.append(blog)
        else :
            if page == None:
                page = 0
            blogs = await myblog.get_blogs_by_page( self.application.db, int(page) )
        body = json.dumps( blogs, default=myblog.Blog_to_json, ensure_ascii=False)
        # blogs = json.loads( body, object_hook=myblog.Blog_from_json)
        logger.debug("service GET:", body )
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write( body )
        self.finish()

    @tornado.web.authenticated
    async def post(self):
        blogs = list()
        id = self.get_argument("id", None) 
        page = self.get_argument("page", None) 
        if id != None :
            blog = await myblog.get_blog_by_id(self.application.db, int(id))
            if blog :
                blogs.append(blog)
        else :
            if page == None:
                page = 0
            blogs = await myblog.get_blogs_by_page( self.application.db, int(page) )
        body = json.dumps( blogs, default=myblog.Blog_to_json, ensure_ascii=False)
        # blogs = json.loads( body, object_hook=myblog.Blog_from_json)
        logger.debug("service:POST: ", body )
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write( body )
        self.finish()
                       
class BlogPostHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self):
        id = self.get_argument("id", None)
        blog = None
        if id:
            blog = await myblog.get_blog_by_id( self.application.db, int(id))
        self.render("post.html", blog= blog)

    @tornado.web.authenticated
    async def post(self):
        contents = self.get_argument("contents", None)
        id = self.get_argument("id", None)
        title = self.get_argument("title", None)
        # update 
        if id:
                # update 
            await myblog.post_update_blog(self.application.db, id, title, contents)    
        else:
                # insert
            await myblog.post_new_blog(self.application.db, self.current_user.id, title, contents)
        self.redirect("/blog/read")

class BlogReadHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self):
        blogs = list()
        id = self.get_argument("id", None) 
        page = self.get_argument("page", None) 
        rpc = self.get_argument("rpc", None) 
        if rpc == 0:
            blogs = self.rpc_get_invoke("/service/read", {'id':id , 'page':page } )
        elif rpc == 1:
            blogs = self.rpc_post_invoke("/service/read", {'id':id , 'page':page } )

        else:
            if id != None :
                blog = await myblog.get_blog_by_id(self.application.db, int(id))
                if blog :
                    blogs.append(blog)
            else :
                if page == None:
                    page = 0
                blogs = await myblog.get_blogs_by_page( self.application.db, int(page) )
        
        self.render("read.html", blogs = blogs )

    async def rpc_get_invoke(self, method, argv):
        rets = None
        server = "http://localhost:8080"
        cookie = self.request.headers['Cookie']
        xsrf = self.get_cookie('_xsrf')
        para = ''
        if len(argv) > 0:
            for k in argv:
                para = para + "&{}={}".format(k, argv[k])
        url = "{}{}?_xsrf={}{}".format(server, method, xsrf, para)
        headers = {'Content-Type': 'application/json; charset=UTF-8','Cookie':cookie}
        response = await tornado.httpclient.AsyncHTTPClient().fetch(url, headers=headers )
        json_str = response.body.decode(errors="ignore")
        rets = json.loads( json_str, object_hook=myblog.Blog_from_json)
        logger.debug("rpc_get_invoke: ",rets)
        return rets

    async def rpc_post_invoke(self, method, argv):
        rets = None
        server = "http://localhost:8080"
        cookie = self.request.headers['Cookie']
        xsrf = self.get_cookie('_xsrf')
        para = ''
        if len(argv) > 0:
            for k in argv:
                para = para + "&{}={}".format(k, argv[k])

        headers = {'Content-Type': 'application/json','Cookie':cookie}
        post_body = json.dumps(argv, ensure_ascii=False)
        url = "{}{}?_xsrf={}".format(server, method, xsrf)
        headers = {'Content-Type': 'application/json; charset=UTF-8', 'Cookie':cookie}
        response = await tornado.httpclient.AsyncHTTPClient().fetch(url, 
            method='POST', body = post_body, headers=headers )
        json_str = response.body.decode(errors="ignore")
        rets = json.loads( json_str, object_hook=myblog.Blog_from_json)
        logger.debug("rpc_post_invoke: ", rets)
        return rets


class LoginModule(tornado.web.UIModule):
    def render(self):
        if self.current_user :
            return '<a href="/auth/logout">Logout</a>'
        else:
            return '<a href="/auth/login">Login</a> / <a href="/auth/create">Create account</a>'

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
        # raise tornado.web.HTTPError(400, "author already created")
        hashed_password = await tornado.ioloop.IOLoop.current().run_in_executor(
            None,
            bcrypt.hashpw,
            tornado.escape.utf8(self.get_argument("password")),
            bcrypt.gensalt(),
        )
       
        email = self.get_argument("email", None)
        name = self.get_argument("name", None)
        uni_hash_passwd = tornado.escape.to_unicode(hashed_password)
        id = await myblog.create_new_user(self.application.db, name, email, uni_hash_passwd)
        if id :
            self.set_secure_cookie("blog_user", "{}|{}".format(str(id), name) )

        self.redirect(self.get_argument("next", "/"))

class AuthLoginHandler(BaseHandler):
    async def get(self):
        next = tornado.escape.url_escape(self.get_argument("next", "/"))
        logger.debug("next = {}".format(next))
        # If there are no authors, redirect to the account creation page.
        if not await self.any_author_exists():
            self.redirect("/auth/create")
        else:
            self.render("login.html", error=None, next=next)

    async def post(self):
        email = self.get_argument("email", None)
        next = self.get_argument("next", "/")
        logger.debug("next = {}".format(next))
        user = await myblog.get_user_by_email(self.application.db, email)
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

    def _log_request(self, handler):

        status = handler.get_status()
        if status < 400:
            if self.settings[r'debug']:
                log_method = logger.debug
            else:
                return
        elif status < 500:
            log_method = logger.warning
        else:
            log_method = logger.error

        log_method(
            r'%d %s %.2fms' % (
                handler.get_status(),
                handler._request_summary(),
                1000.0 * handler.request.request_time()
                )
            )
    

    def __init__(self, db):
        self.db = db
        handlers = [
                    (r'/', IndexHandler), 
                    (r'/blog/post',BlogPostHandler), 
                    (r'/blog/read',BlogReadHandler),
                    (r"/service/read", ServiceHandler),
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
            log_function = self._log_request,
            )
        #[i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
        super(Application, self).__init__(handlers, **settings)

async def main():
    tornado.options.parse_command_line()
    
    # Create the global db connection .
    # sqlite3 block ###################################################################
    dbname = os.path.join(os.path.dirname(__file__), "db", "example.db")
    if options.dbinit > 0 :
        os.remove( dbname)
        os.mkdir(os.path.join(os.path.dirname(__file__), "db"))
    elif os.path.exists( os.path.join(os.path.dirname(__file__), "db") ) == False:
        os.mkdir(os.path.join(os.path.dirname(__file__), "db"))
        options.dbinit = 1
    db = sqlite3.connect( dbname)  #    'example.db')

    # mySQL block ######################################################################
    # 
    #
    #
    # postgreSQL block #################################################################
    # 
    #
    #

    if options.dbinit > 0 :
        myblog.blog_db_init(db)

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

