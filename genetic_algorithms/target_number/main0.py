#!/usr/bin/python
"""
  Application of example from: http://www.ai-junkie.com/ga/intro/gat3.html
"""
import settings

from Genes import Genes
from Selection import Selection
import config


genes=Genes(chromosome_character_nr=config.CHROMOSOMES['CHARACTER_NR'],
              chromosome_character_bits_nr=config.CHROMOSOMES['CHARACTER_BITS']
            )
selection=Selection(genes, 
              target=config.TARGET,
              population_nr=config.GENES['POPULATION_NR'], 
              crossover_probability=config.GENES['CROSSOVER_PROBABILITY'], 
              mutation_probability=config.GENES['MUTATION_PROBABILITY']
            )
solution=Solution(genes, selection, generation_nr)
generations_nr=config.GENERATIONS['NUMBER']
best_generation=None
B_G_T_F_S=0

i=0
while(i<generations_nr):
  try:
    if i%10==0:
      selection.init_population()
      next_generation=selection.population
    else:
      next_generation=selection.make_generation(print_output=False)
    
    print 'GENERATION %i' % i
    print '-------------'
    if i==0:
      C_R_T_F_S=0
      for j in range(len(selection.population)):
        C_R_T_F_S+=selection.population[j].fitness_score
        B_G_T_F_S=C_R_T_F_S
        best_generation=selection.population
      print 'CURRENT GENERATION TOTAL FITNESS SCORE : %s '  % str(C_R_T_F_S)

    N_G_T_F_S=0
    for j in range(len(next_generation)):
      N_G_T_F_S+=next_generation[j].fitness_score
      if N_G_T_F_S>B_G_T_F_S:
        best_generation=next_generation
        B_G_T_F_S=N_G_T_F_S
    
    print 'NEXT GENERATION TOTAL FITNESS SCORE : %s '  % str(N_G_T_F_S)
    print '\n'

    selection.population=next_generation
    i+=1
  except Exception, ex:
    f=open(settings.LOGGING.FILE_REL_PATH, 'a')
    f.write('-------------\n%s\n' % str(ex))
    f.close()

f=open('best_generation.json', 'w')
f.write('\n-------------BEST GENERATION TOTAL FITNESS SCORE : %s \n %s'  % (str(B_G_T_F_S), repr(best_generation)))
f.close()

print '-------------'
print 'Done'
print 'BEST GENERATION TOTAL FITNESS SCORE : %s '  % str(B_G_T_F_S)
print '-------------'

