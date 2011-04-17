#!/usr/bin/python
"""
  Application of example from: http://www.ai-junkie.com/ga/intro/gat3.html
"""
import sys
import os

def do_process(name):
    exec 'from %s import main' % name 
    m = main.main()
    m.compute()
    new_best = m.save()
    if new_best:
      f = open('best_config.json', 'w')
      f.write(str(m.config))
      f.close()

args=[]
for arg in sys.argv: 
    args.append(arg)

if len(args)>2:
    if args[2] == 'config_combinations':
        # create loop with 'all' configuration combinations possible 
        pass
    else:
        i=0
        while i<int(args[2]):
            do_process(args[1])
            i=+1
elif len(args)>1: 
    do_process(args[1])

print '\n\n'
while True:
    print 'Enter a number:'
    ga_pr_dirs = []
    prefix = 'ga_pr_'
    for dirpath,dirnames,filenames in os.walk('./'):
        for _dir in dirnames:
            if _dir.find(prefix)==0:
                ga_pr_dirs.append(_dir)
		i = len(ga_pr_dirs)-1
                print '\t%i. %s' % (i,_dir[len(prefix):]) 

    i = raw_input()
    if not i:
        sys.exit()
    else:
        do_process(ga_pr_dirs[int(i)])
    

