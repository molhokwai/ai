#!/usr/bin/python
"""
  Application of example from: http://www.ai-junkie.com/ga/intro/gat3.html
"""
PROBLEM={
  'ID' : None,
  'NAME' : 'Target Number',
  'DESCRIPTION' : 'Given the digits 0 through 9 and the operators +, -, * and /,  find a sequence that will represent a given target number.',
  'TARGET' : 42  
}

CHROMOSOMES={
  'CHARACTER_NR' : 9,
  'CHARACTER_BITS' : 4
}

GENES={
  'POPULATION_NR' : 10,
  'CROSSOVER_PROBABILITY' : [7,10],
  'MUTATION_PROBABILITY' : [1,1000]
}

GENERATIONS={
  'NUMBER' : 2
}

