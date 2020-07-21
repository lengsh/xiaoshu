#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
from  loguru import logger
import time
import sqlite3
import bcrypt

#logger.add("log.log", retention="1 days", colorize=True, format="<green>{time}</green> <level>{message}</level>")

class Author():
    def __init__(self, id, name, email):
        self.id= id
        self.name = name
        self.email = email

class Bloge():
    def __init__(self, id, uId, title, contents):
        self.id= id
        self.uId = uId
        self.title = title 
        self.contents = contents

if __name__ == "__main__":
    print("test ...")
