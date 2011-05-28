#!/usr/bin/python
"""
  Application of example from: http://www.ai-junkie.com/ga/intro/gat3.html
"""

from Genes import Genes
from Selection import Selection
from Solution import Solution
import config


genes=Genes(chromosome_character_nr=config.CHROMOSOMES['CHARACTER_NR'],
              chromosome_character_bits_nr=config.CHROMOSOMES['CHARACTER_BITS']
            )
selection=Selection(genes, 
              target=config.PROBLEM['TARGET'],
              population_nr=config.GENES['POPULATION_NR'], 
              crossover_probability=config.GENES['CROSSOVER_PROBABILITY'], 
              mutation_probability=config.GENES['MUTATION_PROBABILITY']
            )

solution=Solution(config.PROBLEM,
                  genes, 
                  selection, 
                  nr_of_generations=config.GENERATIONS['NUMBER']
                  )
solution.compute()
solution.save()


print '-------------'
print 'Done'
print 'BEST GENERATION TOTAL FITNESS SCORE : %s '  % str(solution.best_fitness_score)
print '-------------'

