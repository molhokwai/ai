#!/usr/bin/python
"""
  Application of example from: http://www.ai-junkie.com/ga/intro/gat3.html
"""
class Main():
  genes = None
  solution = None
  selection = None
  config = None
  settings = None

  def __init__(self, Genes, Chromosome, Selection, Solution, config, settings):
    self.genes=Genes(chromosome_character_nr=config.CHROMOSOMES['CHARACTER_NR'],
                  chromosome_character_bits_nr=config.CHROMOSOMES['CHARACTER_BITS']
                )
    self.selection=Selection(self.genes, 
                  Chromosome,
                  target=config.PROBLEM['TARGET'],
                  population_nr=config.GENES['POPULATION_NR'], 
                  crossover_probability=config.GENES['CROSSOVER_PROBABILITY'], 
                  mutation_probability=config.GENES['MUTATION_PROBABILITY']
                )

    self.solution=Solution(
                  config.PROBLEM,
                  self.genes, 
                  self.selection, 
                  nr_of_generations=config.GENERATIONS['NUMBER'],
		  settings=settings
                )

    self.config = config 
    self.settings = settings

    print '-------------'
    print 'CONFIGURATION'
    print '\tPROBLEM : %s '  % str(self.config.PROBLEM)
    print '\tCHROMOSOMES : %s '  % str(self.config.CHROMOSOMES)
    print '\tGENES : %s '  % str(self.config.GENES)
    print '\tGENERATIONS : %s '  % str(self.config.GENERATIONS)
    print '-------------\n'


  def compute(self):
    self.solution.compute()
    
    print '-------------'
    print 'Done'
    print 'BEST GENERATION TOTAL FITNESS SCORE : %s '  % str(self.solution.best_fitness_score)
    print '-------------\n'

  def save(self):
    from Db import Db as Db
    saved = Db(self.settings).save(self.solution, self.config)
    
    print '-------------'
    print 'Save done (%s)' % ('new best solution' if saved else 'no db.write, not best solution')
    print '-------------\n'

    if saved:
      return self.solution.best_fitness_score
