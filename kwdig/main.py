#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.template as template
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.locks
import tornado.web
import time
from tornado import gen
import tornado.httpclient
#import bcrypt
import signal
import aiomysql
import logging
import shutil

import dbmodel
import dig
import mypatent as mp

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from tornado.options import  options,define 
define("port",default=8080,help="server listen port", type=int)
define("dbinit",default=0,help="if need to init db, 0:No; 1:Yes", type=int)

class BaseHandler(tornado.web.RequestHandler):
    async def prepare(self):
        pass
         # get_current_user cannot be a coroutine, so set
         # self.current_user in prepare instead.

class IndexHandler(BaseHandler):
    async def get(self):
        self.render('index.html' )

class RedigHandler(BaseHandler):
    async def get(self):
        docid = self.get_argument("docid", 0)
        filename = await mp.get_document_filename(self.application.db, int(docid))
        if filename == None:
            self.render("info.html", infoMsg = "this docid is not exist! ")
        else:
            filepath = os.path.join(self.application.docpath, filename)
            if os.path.exists(filepath):
                await mp.delete_document(self.application.db, int(docid), False)
                await dig.Process(self.application.db, filepath) 
                self.redirect("/dig?docid="+docid)
            else:
                msg = filepath + " is not exist! please upload again!"
                self.render("info.html", infoMsg= msg )


class WdictHandler(BaseHandler):
    async def get(self):
        cmd = self.get_argument("cmd", None)
        id = self.get_argument("id", None)
        kw = self.get_argument("kw", None)
        if cmd == 'ADD' and kw != None and len(kw) > 1 :
            await mp.add_omit_word(self.application.db, kw)
            #print("add ", kw)
        elif cmd == 'DEL' and id != None and int(id) > 0:
            await mp.delete_omit_word(self.application.db, int(id))
            #print("delete id=", id) 

        w_dict =await mp.get_all_omit_words(self.application.db )
        #for r in w_dict:
        #    print(r)
        self.render("dict.html", dicts= w_dict )


    async def post(self):
        kw = self.get_argument("kw", None)
        cmd = self.get_argument("cmd", None)
        id = self.get_argument("id", None)
        if cmd == 'ADD' and kw != None and len(kw) > 1 :
            await mp.add_omit_word(self.application.db, kw)
        #    print("add ", kw)
        elif cmd == 'DEL' and id != None and int(id) > 0:
            await mp.delete_omit_word(self.application.db, int(id))
        #    print("delete id=", id) 

        w_dict = await mp.get_all_omit_words(self.application.db )
        self.render("dict.html", dicts= w_dict )

class PdictHandler(BaseHandler):
    async def get(self):
        cmd = self.get_argument("cmd", None)
        id = self.get_argument("id", None)
        kw = self.get_argument("kw", None)
        if cmd == 'ADD' and kw != None and len(kw) > 1 :
            await mp.add_omit_phrase(self.application.db, kw)
        #    print("add ", kw)
        elif cmd == 'DEL' and id != None and int(id) > 0:
            await mp.delete_omit_phrase(self.application.db, int(id))
        #    print("delete id=", id) 

        w_dict = await mp.get_all_omit_phrases(self.application.db )
        # for r in w_dict:
        #     print(r)
        self.render("pdict.html", dicts= w_dict )


    async def post(self):
        kw = self.get_argument("kw", None)
        cmd = self.get_argument("cmd", None)
        id = self.get_argument("id", None)
        if cmd == 'ADD' and kw != None and len(kw) > 1 :
            await mp.add_omit_phrase(self.application.db, kw)
        #    print("add ", kw)
        elif cmd == 'DEL' and id != None and int(id) > 0:
            await mp.delete_omit_phrase(self.application.db, int(id))
        #    print("delete id=", id) 

        w_dict = await mp.get_all_omit_phrases(self.application.db )
        self.render("pdict.html", dicts= w_dict )


class KwdictHandler(BaseHandler):
    async def get(self):
        dicts = await mp.get_all_keywords(self.application.db )
        self.render("kwdict.html", dicts=dicts)

    async def post(self):
        docId = self.get_argument("id", 0)
        dicts = await mp.get_all_doc_kw_words(self.application.db, docId )
        # for r in w_dict:
        #     print(r)
        self.render("kwdict.html", dicts= dicts )

class KwEditHandler(BaseHandler):
    async def get(self):
        errMsg = ""
        id = self.get_argument("id", 0)
        kw = self.get_argument("kw", "")
        cmd = self.get_argument("cmd", "")
        descr = self.get_argument("descr", "").strip()
        if cmd.upper() == "ADD" and len(kw) > 0:
            kw = kw.lower()
            await mp.add_keyword(self.application.db, kw, descr)
            dicts = await mp.get_all_keywords(self.application.db, 1)
            self.render("kwdict.html", dicts =dicts)
            return

        elif cmd.upper() == "UPIT" and len(kw) > 0 and int(id)>0 :
            await mp.update_keyword(self.application.db, int(id), kw.lower(), descr)
            dicts = await mp.get_all_keywords(self.application.db )
            self.render("kwdict.html", dicts=dicts)
            return
        
        if cmd.upper() == "EDIT" and int(id)>0 :
            ob = await mp.get_keyword(self.application.db, int(id))
            cmd = "UPIT"
            if ob.id:
                kw = ob.word.lower()
                descr = ob.descr.strip()
        self.render("kwedit.html", kw = kw, descr = descr, cmd=cmd, id=id, errMsg = errMsg)

    async def post(self):
        errMsg = ""
        id = self.get_argument("id", 0)
        kw = self.get_argument("kw", "")
        cmd = self.get_argument("cmd", "")
        descr = self.get_argument("descr", "").strip()
        if cmd.upper() == "ADD" and len(kw) > 0:
            await mp.add_keyword(self.application.db, kw, descr)
            dicts = await mp.get_all_keywords(self.application.db, 1)
            self.render("kwdict.html", dicts=dicts)
            return

        elif cmd.upper() == "UPIT" and len(kw) > 0 and int(id)>0 :
            await mp.update_keyword(self.application.db, int(id), kw, descr)
            dicts = await mp.get_all_keywords(self.application.db )
            self.render("kwdict.html", dicts=dicts)
            return
        
        if cmd.upper() == "EDIT" and int(id)>0 :
            ob = await mp.get_keyword(self.application.db, int(id))
            cmd = "UPIT"
            if ob.id:
                kw = ob.word
                descr = ob.descr.strip()
        self.render("kwedit.html", kw = kw, descr = descr, cmd=cmd, id=id, errMsg = errMsg)

class DocEditHandler(BaseHandler):
    async def get(self):
        errMsg = ""
        fn = ""
        descr = ""
        id = self.get_argument("id", 0)
        if int(id)>0 :
            fn,descr = await mp.get_document_file(self.application.db, int(id))
            if fn == None:
                errMsg = "此文档不存在！"
        else:
            errMsg = "文档ID格式不正确！"
        self.render("docedit.html", fn=fn, descr = descr, id=id, errMsg = errMsg)

    async def post(self):
        errMsg = ""
        id = self.get_argument("id", 0)
        descr = self.get_argument("descr", "").strip()
        if len(descr) > 0:    
            await mp.edit_document(self.application.db, id, descr)
            errMsg="Update successful!"
        fn = ""
        fn, descr = await mp.get_document_file(self.application.db, id)
        self.render("docedit.html", fn = fn, descr = descr, id=id, errMsg = errMsg)


class DigHandler(BaseHandler):
    async def get(self):
        docid = self.get_argument("docid", None)
        id = self.get_argument("id", None)
        cmd = self.get_argument("cmd", None)
        topic = self.get_argument("tp", None)
        kw = self.get_argument("kw", None)

        if cmd == 'DAA' and int(id) > 0 and topic != None and kw != None:
            if topic == 'W':
                await mp.add_omit_word(self.application.db, kw )
                await mp.delete_doc_word(self.application.db, int(id))
            elif topic == 'P':
                await mp.add_omit_phrase(self.application.db, kw ) 
                await mp.delete_doc_phrase(self.application.db, int(id))

        if cmd == 'DEL' and id != None and int(id) > 0 and topic != None:
            if topic == 'W':
                await mp.delete_doc_word(self.application.db, int(id))
            elif topic == 'P':
                await mp.delete_doc_phrase(self.application.db, int(id))
            elif topic == 'K':
                await mp.delete_doc_kw_word(self.application.db, int(id))

        kws = await mp.get_all_doc_kw_words(self.application.db, docid)
        wds = await mp.get_words_by_docId(self.application.db, docid)
        phs = await mp.get_phrases_by_docId(self.application.db, docid)
        self.render("dig.html", wdicts= wds, pdicts = phs, kdicts = kws, docid=docid )

    async def post(self):
        docid = self.get_argument("docid", None)
        id = self.get_argument("id", None)
        cmd = self.get_argument("cmd", None)
        topic = self.get_argument("tp", None)
        kw = self.get_argument("kw", None)

        if cmd == 'DAA' and int(id) > 0 and topic != None and kw != None:
            if topic == 'W':
                await mp.add_omit_word(self.application.db, kw )
                await mp.delete_doc_word(self.application.db, int(id))
            elif topic == 'P':
                await mp.add_omit_phrase(self.application.db, kw ) 
                await mp.delete_doc_phrase(self.application.db, int(id))

        if cmd == 'DEL' and id != None and int(id) > 0 and topic != None:
            if topic == 'W':
                await mp.delete_doc_word(self.application.db, int(id))
            elif topic == 'P':
                await mp.delete_doc_phrase(self.application.db, int(id))

        kws = await map.get_all_doc_kw_words(self.application.db, docid)
        wds = await mp.get_words_by_docId(self.application.db, docid)
        phs = await mp.get_phrases_by_docId(self.application.db, docid)
        self.render("dig.html", wdicts= wds, pdicts = phs, kdicts = kws, docid=docid )


class DocsHandler(BaseHandler):
    async def get(self):
        docid = self.get_argument("docid", None)
        page = self.get_argument("page", 0)
        cmd = self.get_argument("cmd", None)
        if cmd == 'DEL' and docid != None and int(docid) > 0:
            await mp.delete_document(self.application.db, int(docid))
            #print("delete document docid=", docid) 

        docs = await mp.get_all_documents(self.application.db, int(page)*100)
        self.render("document.html", docs= docs )


    async def post(self):
        docid = self.get_argument("docid", None)
        page = self.get_argument("page", 0)
        cmd = self.get_argument("cmd", None)
        if cmd == 'DEL' and docid != None and int(docid) > 0:
            await mp.delete_document(self.application.db, int(docid))
            #print("delete document docid=", docid) 

        docs = await mp.get_all_documents(self.application.db, int(page)*100)
        self.render("document.html", docs= docs )

class FileHandler(BaseHandler):
    async def get(self):
        self.render("upload.html", errMsg= "" )

    async def post(self):
        errMsg = "" 
        uppath = self.application.docpath
        # print("upload_path = ", uppath)
        if len(self.request.files) == 0:
            errMsg = "No files"
        meta = self.request.files['docfile'][0]
        filename = meta['filename']
        filepath = os.path.join(uppath, filename)
        suffix = filename.split('.')[-1]

        if suffix != "doc" and suffix != 'DOC' and suffix != 'docx' and suffix != 'DOCX':
            errMsg = filename + " is not word document!"
        if os.path.exists(filepath):
            errMsg = filename + " is exists in upload path"  
        if len(errMsg) <= 0:
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
                errMsg = errMsg + filename + "sucessful!"

            if suffix == "doc" or suffix == 'DOC':
                cmd = 'libreoffice --headless --convert-to docx '+ filepath
                os.system(r""+cmd)
                f_src = os.path.basename( filepath )
                f_src = f_src.replace(suffix, "docx")
                # print("move ", f_src, " to ", self.application.docpath)
                shutil.move(f_src,  self.application.docpath)
                filepath = os.path.join(self.application.docpath, f_src)  
            await dig.Process(self.application.db, filepath) 
            self.redirect("/docs")
        else:
            self.render("upload.html", errMsg= errMsg )

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
    

    def __init__(self, db, docpath="upload"):
        self.db = db
        self.docpath= os.path.join(os.getcwd(), "static", docpath)
        handlers = [
                    (r'/', IndexHandler), 
                    (r'/wdict',WdictHandler),
                    (r'/pdict',PdictHandler),
                    (r'/kwdict',KwdictHandler),
                    (r'/kwedit',KwEditHandler),
                    (r'/docedit',DocEditHandler),
                    (r'/docs', DocsHandler),
                    (r'/dig', DigHandler),
                    (r'/redig',RedigHandler),
                    (r'/upload', FileHandler)
        ]

        settings = dict(
            web_title=u"Patent Digger",
            template_path=os.path.join(os.path.dirname(__file__), "html"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={},
            xsrf_cookies=True,
            cookie_secret="__TODO:_YOUR_OWN_RANDOM_VALUE_HERE__ABCDEFG.......",
            login_url= None, 
            debug=True,
            log_function = self._log_request,
            )
        super(Application, self).__init__(handlers, **settings)

async def main():
    tornado.options.parse_command_line()
    db = await aiomysql.connect(host='127.0.0.1', port=3306, user='lengsh', password='123456', db='patent', charset="utf8mb4")
    
    if options.dbinit > 0 :
        await myblog.blog_db_init(db)

    app = Application(db)
    app.listen(options.port)
        # In this demo the server will simply run until interrupted
        # with Ctrl-C, but if you want to shut down more gracefully,
        # call shutdown_event.set().
    shutdown_event = tornado.locks.Event()
    def shutdown( signum, frame ):

        print("graceful shutdown?!!!! signum={}".format(signum))
        print("clear all memery and  shutdown  database !!!!")
        db.close()
        shutdown_event.set()


    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    await shutdown_event.wait()
    print("\n\nshutdown -h now\n\n")

if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)

