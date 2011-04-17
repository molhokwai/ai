#!/usr/bin/python

class Generation:
  fitness_score=0
  chromosomes=[]

class Solution:
  _best_generation=None
  _best_fitness_score=None
  
  problem=None
  genes=None
  selection=None
  nr_of_generations=None
  settings=None  

  def __init__(self, problem, genes, selection, nr_of_generations=1000, settings=settings):
    self.problem=problem
    self.genes=genes
    self.selection=selection
    self.nr_of_generations=nr_of_generations
    self.settings=settings

  @property
  def best_generation(self):
    return self._best_generation

  @property
  def best_fitness_score(self):
    return self._best_fitness_score

  def compute(self):
    self._best_generation=Generation()
    i=0
    while(i<self.nr_of_generations):
      try:
        print 'GENERATION %i' % i
        print '-------------'

        if i%10==0:
          self.selection.init_population()
          next_generation=self.selection.population
        else:
          next_generation=self.selection.make_generation(print_output=False)
        
        if i==0:
          C_R_T_F_S=0
          for j in range(len(self.selection.population)):
            p_f_s = self.selection.population[j].fitness_score
            if p_f_s:
              C_R_T_F_S+=p_f_s

          self._best_generation.fitness_score=C_R_T_F_S
          self._best_generation.chromosomes=self.selection.population
          self._best_fitness_score=C_R_T_F_S
          print 'CURRENT GENERATION TOTAL FITNESS SCORE : %s '  % str(C_R_T_F_S)

        N_G_T_F_S=0
        for j in range(len(next_generation)):
          p_f_s = next_generation[j].fitness_score
          if p_f_s:
            N_G_T_F_S+=p_f_s

        if N_G_T_F_S>self._best_generation.fitness_score:
          self._best_generation.chromosomes=next_generation
          self._best_generation.fitness_score=N_G_T_F_S
          self._best_fitness_score=N_G_T_F_S
        
        print 'NEXT GENERATION TOTAL FITNESS SCORE : %s '  % str(N_G_T_F_S)
        print '\n'

        self.selection.population=next_generation
        i+=1
      except Exception, ex:
        f=open(self.settings.LOGGING['FILE_REL_PATH'], 'a')
        f.write('-------------base/Solution.py')
        f.write('-------------\n%s\n' % str(ex))
        f.close()
        
