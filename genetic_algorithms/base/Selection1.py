#!/usr/bin/python
"""
  Application of example from: http://www.ai-junkie.com/ga/intro/gat3.html

  IMPLEMENT MULTITHREADING
     - AT THE LEVEL OF THE ROULETTE WHEEL
     - AT THE LEVEL OF THE POPULATION MAKING
  ...USING PYTHON Threading MODULE
"""
import math
import random
import threading
import time
random.seed()

from  Chromosome import Chromosome
from Genes import Genes

exit_flag = 0
def print_time(threadName, delay, counter):
	while counter:
		if exit_flag:
			thread.exit()
 			time.sleep(delay)
			print "%s: %s" % (threadName, time.ctime(time.time()))
			counter -= 1

class SThread(threading.Thread):
	threadID = None
	name = None
	counter = 0

	def __init__(self, threadID, name, counter):
		self.threadID = threadID
		self.name = name
		self.counter = counter
		threading.Thread.__init__(self)
    
	def run(self, _function, *args):
		print "Starting " + self.name
		print_time(self.name, self.counter, 5)
		function(args)
		print "Exiting " + self.name

class Selection():
  genes=None
  
  target=42
  population_nr=1000  
  crossover_probability=[7,10]
  mutation_probability=[1,1000]

  _population=[]

  def __init__(self, genes, target=42, population_nr=1000,
              crossover_probability=[7,10], mutation_probability=[1,1000]):
    self.genes=genes
    self.target=target
    self.population_nr=population_nr  
    self.crossover_probability=crossover_probability
    self.mutation_probability=mutation_probability

  def init_population(self):
    """First population initialization, or poopulation reset"""
    self._population=[]
    for i in range(self.population_nr):
      bits=''
      for j in range(self.genes.chromosome_bits_nr):
        bits+=str(random.choice([0,1]))

      chromosome=Chromosome(self.genes, 23, bits)
      self._population.append(chromosome)
  
  @property
  def population(self):
    return self._population
  

  def make_generation(self, print_output=True):
    """Next generation making, with roulette wheel, crossover, and mutation"""
    def threading_function(self):
			if print_output:
				print '\n'
				print 'ROULETTE WHEEL'
			pair=self.roulette_wheel()
			if print_output: print repr(pair)
			
			_do, pair=self.crossover(pair)
			if print_output: 
				print '\n\n'
				print 'DO CROSSOVER : %s ' % str(_do)
				print repr(pair)

			if _do:
				if print_output:
					print '\n\n'
					print 'DO MUTATION : %s ' % str(_do)
				_do, pair=self.mutation(pair)
				if print_output:
					print repr(pair)

			if len(_population)<len(self.population):	
				_population.append(pair[0])
				_population.append(pair[1])

    _population=[]
    _sthreads=[]
		counter
    while(len(_population)<len(self.population)):
      l_p = len(_population)
      l_s_p = len(self.population)
      n = 100 if l+100<=l_s_p else l_s_p - l_p
      if len(filter(lambda x: x.isAlive(), _sthreads))==0:
				i = 0
				while i<n:
					sthread = SThread(i, 'make_gen_thread_%i' %i, counter+i)
					sthread.run(threading_function(self))
					_sthreads.append(sthread)
					i+=1

    if print_output:
      print '\n\n'

    return _population


  def roulette_wheel(self):
    """ ROULETTE WHEEL """
    _roulette_wheel=[]
    cursor=0
    for i in range(len(self.population)):
      chromo=self.population[i]
      _roulette_wheel.append([cursor, chromo])
      cursor+=chromo.fitness_score
      
    pair=[]
    while(len(pair)<2):
      rand=random.randrange(0, math.ceil(cursor), 1)
      selection=filter(lambda x: x[0]>rand-0.5 and x[0]>rand+0.5, _roulette_wheel)
      if len(selection)>0:
        pair.append(selection[0][1])
        if len(selection)>1:
          pair.append(selection[1][1])
    return pair


  def crossover(self, pair):
    """ CROSSOVER"""
    # probability: 0.7
    # strict(?)
    _do=random.choice([True if j<=self.crossover_probability[0] else False for j in range(len(self.crossover_probability))])
    # loose(?)
    # _do=random.choice([j for j in range(11)])>3
    if _do:
      i=random.randrange(0, self.genes.chromosome_bits_nr-1, 1)
      chr_bits=[[pair[0].bits[j:j+1] for j in range(self.genes.chromosome_bits_nr)], 
                [pair[1].bits[j:j+1] for j in range(self.genes.chromosome_bits_nr)]]
      while(i<self.genes.chromosome_bits_nr):
        c0_b=chr_bits[0][i]
        chr_bits[0][i]=chr_bits[1][i]
        chr_bits[1][i]=c0_b
        i+=1
      pair[0].bits=''.join(chr_bits[0])
      pair[1].bits=''.join(chr_bits[1])
    return _do,pair


  def mutation(self, pair):
    """ MUTATION """
    def flip(x): return '0' if x=='1' else '1'

    # probability: 0.001
    # strict(?)
    _do=random.choice([True if j<=self.mutation_probability[0] else False for j in range(len(self.mutation_probability))])
    # loose(?)
    # _do=random.choice([j for j in range(1001)])==500
    if _do:
      i=random.randrange(0, self.genes.chromosome_bits_nr-1, 1)
      chr_bits=[[pair[0].bits[j:j+1] for j in range(self.genes.chromosome_bits_nr)], 
                [pair[1].bits[j:j+1] for j in range(self.genes.chromosome_bits_nr)]]
      while(i<self.genes.chromosome_bits_nr):
        c0_b=chr_bits[0][i]
        chr_bits[0]=map(flip, chr_bits[0])
        chr_bits[1]=map(flip, chr_bits[1])
        i+=1
      pair[0].bits=''.join(chr_bits[0])
      pair[1].bits=''.join(chr_bits[1])
    return _do,pair



