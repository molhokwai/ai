#!/usr/bin/python
from db import Da as Da

class Db:
  settings = None
  
  def __init__(self, settings):
    self.settings = settings
    
  def save(self, solution, config):
    da = Da(self.settings)
    
    chromosomes=[]
    for i in range(solution.selection.population_nr):
      chromo=da.execute('SELECT * FROM Chromosome WHERE bits=?', 'r', parameters=[str(solution.best_generation.chromosomes[i].bits)])
      if not chromo:
        da.execute('INSERT INTO Chromosome(bits) VALUES(?)', 'c', parameters=[str(solution.best_generation.chromosomes[i].bits)])
        chromo=da.execute('SELECT * FROM Chromosome WHERE bits=?', 'r', parameters=[str(solution.best_generation.chromosomes[i].bits)])
      chromosomes.append(chromo)
    
    problem_row=da.execute('SELECT * FROM Problem WHERE name=? and target=?', 'r', parameters=[solution.problem['NAME'], str(solution.problem['TARGET'])])
    if not problem_row:
      da.execute('INSERT INTO Problem(name, description, target) VALUES(?, ?, ?)', 'c', parameters=[solution.problem['NAME'], solution.problem['DESCRIPTION'], str(solution.problem['TARGET'])])
      problem_row=da.execute('SELECT * FROM Problem WHERE name=? and target=?', 'r', parameters=[solution.problem['NAME'], str(solution.problem['TARGET'])])

    solution.problem['ID']=int(problem_row[3])    
    prv_best_fitness_score=0
    generation=da.execute('SELECT * FROM Solution WHERE Problem=?', 'r', parameters=[solution.problem['ID']])
    if generation:
      for i in range(len(generation)): prv_best_fitness_score+=generation[i][2]

    if solution.best_generation.fitness_score>prv_best_fitness_score:
        solution.best_fitness_score=solution.best_generation.fitness_score
        da.execute('DELETE FROM Solution WHERE Problem=?', 'd', parameters=[solution.problem['ID']])
        tuples=[]
        for i in range(solution.selection.population_nr):
          tuples.append(
                (
                  solution.problem['ID'],
                  int(chromosomes[i][1]),
                  float(solution.best_generation.chromosomes[i].fitness_score),
                  solution.best_generation.chromosomes[i].sequence,
                  solution.best_generation.chromosomes[i].solution
                )
          )
        da.bulk_execute(
          'INSERT INTO Solution(Problem, Chromosome, fitness_score, sequence, solution) VALUES(?, ?, ?, ?, ?) ', 'c', tuples=tuples)

        best_solution_config = """{
          \n\t'CONFIGURATION':{
              \n\t\t'PROBLEM : %s '
              \n\t\t'CHROMOSOMES : %s '
              \n\t\t'GENES : %s '
              \n\t\t'GENERATIONS : %s '
          \n\t}
        \n}'""" % (str(config.PROBLEM), 
	        str(config.CHROMOSOMES),
	        str(config.GENES),
	        str(config.GENERATIONS))
        da.execute('UPDATE Problem SET best_solution_config = ? WHERE id = ?', 'u', parameters=[best_solution_config, solution.problem['ID']])

        return True 
    else:
        solution.best_fitness_score=prv_best_fitness_score
        return False
    da.close()

