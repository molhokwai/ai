#!/usr/bin/python
"""
  Application of example from: http://www.ai-junkie.com/ga/intro/gat3.html
"""
import sys

args=[]
for arg in sys.argv: 
    args.append(arg)

exec 'from %s import main' % args[1]
m = main.main()
m.compute()
m.save()


