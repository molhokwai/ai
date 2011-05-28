# base from http://www.student.nada.kth.se/~d94-tan/notes/tkcanvas/tkcanvas.htm
# modified

"""
   Non overlapping
   Check overlapping: Trace a vector between the 2 centers and check if the radiuses overlap
    Vl  : Vector Length
    r1, r2  : Circle one, Circle two radius
    VL = square_root((C1x - C2x)^2 + (C1y + C2y)^2)
    overlap = (C1r + C2r)>Vl
"""
import math
import random
import time

from Tkinter import *

def overlap(canvas, o1, o2):
  if len(canvas.coords(o1))>0 and len(canvas.coords(o2))>0:
      o1x = canvas.coords(o1)[0]
      o1y = canvas.coords(o1)[1]
      r1 = canvas.coords(o1)[2]-canvas.coords(o1)[0]
      
      o2x = canvas.coords(o2)[0]
      o2y = canvas.coords(o2)[1]
      r2 = canvas.coords(o2)[2]-canvas.coords(o2)[0]
      
      f=open('log.l', 'a')
      f.write('ovals : %s\n' % str(ovals))
      f.write('%s > %s\n' % (str(r1 + r2), str(math.sqrt(math.pow(o1x - o2x,2) + math.pow(o1y - o2y,2)))))
      f.write('%s \n\n' % str(r1 + r2 > math.sqrt(math.pow(o1x - o2x,2) + math.pow(o1y - o2y,2))))
      f.close()
                            
      return r1 + r2 > math.sqrt(math.pow(o1x - o2x,2) + math.pow(o1y - o2y,2))


nr = 200
ovals=[]

w = Tk()
c = Canvas(w, height=500, width=500, background="white")

i=0
while i<nr:
    r=random.randrange(20, 250, 10)
    x=random.randrange(20, 1000, 10)
    y=random.randrange(20, 1000, 10)
    if r+x<500 and r+y<500:
        o = c.create_oval(x,y,x+r,y+r, outline="black")
        if i==0: 
          ovals.append(o)
          i+=1
        else:
            for j in range(len(ovals)):
                if not overlap(c, o, ovals[j]):
                    if o not in ovals:
                        ovals.append(o)
                        i+=1
                else:
                    c.delete(o)    

f=open('ovals.l', 'w')
f.write('[')
for i in range(len(ovals)):
    if i>0: 
        f.write(',\n')
    if len(c.coords(ovals[i]))>0:
        f.write('  {%s : %s}' % (ovals[i], str(c.coords(ovals[i]))))
f.write(']')
f.close()

c.pack()
w.mainloop()

