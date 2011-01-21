#!/usr/bin/python
"""
  Application of example from: http://www.ai-junkie.com/ga/intro/gat3.html
"""
class Main():
  genes = None
  solution = None
  selection = None
  settings = None

  def __init__(self, Genes, Selection, Solution, config, settings):
    self.genes=Genes(chromosome_character_nr=config.CHROMOSOMES['CHARACTER_NR'],
                  chromosome_character_bits_nr=config.CHROMOSOMES['CHARACTER_BITS']
                )
    self.selection=Selection(self.genes, 
                  target=config.PROBLEM['TARGET'],
                  population_nr=config.GENES['POPULATION_NR'], 
                  crossover_probability=config.GENES['CROSSOVER_PROBABILITY'], 
                  mutation_probability=config.GENES['MUTATION_PROBABILITY']
                )

    self.solution=Solution(
                  config.PROBLEM,
                  self.genes, 
                  self.selection, 
                  nr_of_generations=config.GENERATIONS['NUMBER']
                )

    self.settings = settings

  def compute(self):
    self.solution.compute()
    
    print '-------------'
    print 'Done'
    print 'BEST GENERATION TOTAL FITNESS SCORE : %s '  % str(self.solution.best_fitness_score)
    print '-------------\n'

  def save(self):
    from Db import Db as Db
    Db(self.settings).save(self.solution)
    
    print '-------------'
    print 'Save done'
    print '-------------\n'

