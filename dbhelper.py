# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 16:03:12 2017

@author: Ignasi Dev
"""
import sqlite3

class DBHelper:

    # Create a database connection given a database name (taskbot):
    def __init__(self, dbname = "taskbot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # Create table items with one column: desriptiuon:
    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    # Insert the text into the db table:
    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    # Removes an item (given in text) from the db:
    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]
