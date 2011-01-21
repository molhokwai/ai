#!/usr/bin/python
import sqlite3
import settings

def init():
  con = sqlite3.connect(settings.DB['FILE_PATH'])
  con.isolation_level = None
  cur = con.cursor()
  return con, cur

def close(con):
  con.close()

def execute(query, crud, parameters=None):
  con, cur = init()
  result=None
  if (parameters):
    result=cur.execute(query, parameters)
  else:
    result=cur.execute(query)

  
  if crud=='r':
    result=cur.fetchall()
    if result:
      if len(result)==1: return result[0]
  close(con)
  
  return result

def bulk_execute(query, crud, tuples=None):
  con, cur = init()
  result=None
  for i in range(len(tuples)):
    result=cur.execute(query, tuples[i])
  
  return result
