#!/usr/bin/python
import settings

class Generation:
  fitness_score=0
  chromosomes=[]

class Solution:
  _best_generation=None
  
  problem=None
  genes=None
  selection=None
  nr_of_generations=None
  
  def __init__(self, problem, genes, selection, nr_of_generations=1000):
    self.problem=problem
    self.genes=genes
    self.selection=selection
    self.nr_of_generations=nr_of_generations

  @property
  def best_generation(self):
    return self._best_generation

  def compute(self):
    self._best_generation=Generation()
    i=0
    while(i<self.nr_of_generations):
      try:
        if i%10==0:
          self.selection.init_population()
          next_generation=self.selection.population
        else:
          next_generation=self.selection.make_generation(print_output=False)
        
        print 'GENERATION %i' % i
        print '-------------'
        if i==0:
          C_R_T_F_S=0
          for j in range(len(self.selection.population)):
            C_R_T_F_S+=self.selection.population[j].fitness_score
            self.best_generation.fitness_score=C_R_T_F_S
            self.best_generation.chromosomes=self.selection.population
          print 'CURRENT GENERATION TOTAL FITNESS SCORE : %s '  % str(C_R_T_F_S)

        N_G_T_F_S=0
        for j in range(len(next_generation)):
          N_G_T_F_S+=next_generation[j].fitness_score
          if N_G_T_F_S>self.best_generation.fitness_score:
            self.best_generation.chromosomes=next_generation
            self.best_generation.fitness_score=N_G_T_F_S
        
        print 'NEXT GENERATION TOTAL FITNESS SCORE : %s '  % str(N_G_T_F_S)
        print '\n'

        self.selection.population=next_generation
        i+=1
      except Exception, ex:
        f=open(settings.LOGGING.FILE_REL_PATH, 'a')
        f.write('-------------\n%s\n' % str(ex))
        f.close()
    
  def save(self):
    import db
    chromosomes=[]
    for i in range(self.selection.population_nr):
      chromo=db.execute('SELECT * FROM Chromosome WHERE bits=%s' % self.best_generation.chromosomes[i].bits, 'r')
      if not chromo:
        db.execute('INSERT INTO Chromosome(bits) VALUES(%s)' % self.best_generation.chromosomes[i].bits, 'c')
        chromo=db.execute('SELECT * FROM Chromosome WHERE bits=%s' % self.best_generation.chromosomes[i].bits, 'r')
      chromosomes.append(chromo)
    
    problem=db.execute('SELECT * FROM Problem WHERE name=%s and target=%s' % (self.problem['NAME'], str(self.problem['TARGET'])), 'r')
    if not problem:
      db.execute('INSERT INTO Problem(name, description, target) VALUES(%s, %s, %s)' % (self.problem['NAME'], self.problem['DESCRIPTION'], str(self.problem['TARGET'])), 'c')
      problem=db.execute('SELECT * FROM Problem WHERE name=%s and target=%s' % (self.problem['NAME'], str(self.problem['TARGET'])), 'r')
    
    prv_fitness_score=0
    generation=db.execute('SELECT * FROM Solution WHERE Problem=%i' % int(problem['id']), 'r')
    if generation:
      for i in range(generation): prv_fitness_score+=generation[j].fitness_score
    
    if self.best_generation.fitness_score>prv_fitness_score:
        db.execute('DELETE FROM Solution WHERE Problem=%i' % int(problem['id']), 'd')
        tuples=[]
        for i in range(self.selection.population_nr):
          tuples.append((int(problem['id']), 
                  int(chromosomes[i]['id']), 
                  float(self.best_generation.chromosomes[i].fitness_score),
                  self.best_generation.chromosomes[i].sequence,
                  self.best_generation.chromosomes[i].solution
                  ))
        db.bulk_execute(
          'INSERT INTO Solution(Problem, Chromosome, fitness_score, sequence, solution) Chromosome(?, ?, ?, ?, ?) ', 'c', tuples)

"""
def save(self):
  chromosomes=[]
  while(i<self.nr_of_generations):
    chromo=wrapper.select('chromosome %s' % self.best_generation.chromosomes[i].bits)
    if not chromo:
      wrapper.insert('chromosome %s' % self.best_generation.chromosomes[i])
      chromo=wrapper.select('chromosome %s' % self.best_generation.chromosomes[i].bits)
  chromosomes.append(chromo)
  
  problem=wrapper.fetchone('problem %s ' % self.problem.NAME)
  if not problem:
    wrapper.insert('chromosomes  %s' % self.problem)
  problem=wrapper.fetchone('problem %s ' % self.problem.NAME)
  
  prv_fitness_score=0
  generation=wrapper.select('solution where problem %i ' % problem.id)
  if generation:
    t=0
    for j in range(len(generation)): prv_fitness_score+=generation[j].fitness_score
  
  if self.generation.fitness_score>prv_fitness_score:
      wrapper.delete('solution where problem %i' % problem.id)
      wrapper.bulk_insert('solution with chromosomes %a, problem %i' % (chromosomes, problem.id))

"""
