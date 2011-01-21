#!/usr/bin/python
import sqlite3

class Da():
  con = None
  cur = None

  def __init__(self, settings):
    self.con = sqlite3.connect(settings.DB['FILE_PATH'])
    self.con.isolation_level = None
    self.cur = self.con.cursor()

  def __del__(self):
    self.con.close()
  
  def close(self):
    self.con.close()

  def execute(self, query, crud, parameters=None):
    result=None
    if (parameters):
      result=self.cur.execute(query, parameters)
    else:
      result=self.cur.execute(query)
    
    if crud=='r':
      result=self.cur.fetchall()
      if result:
        if len(result)==1: return result[0]
    
    return result

  def bulk_execute(self, query, crud, tuples=None):
    result=None
    for i in range(len(tuples)):
      result=self.cur.execute(query, tuples[i])
    
    return result

