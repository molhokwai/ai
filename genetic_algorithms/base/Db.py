#!/usr/bin/python
class Db:
    
  @staticmethod
  def save(solution):
    import db
    chromosomes=[]
    for i in range(solution.selection.population_nr):
      chromo=db.execute('SELECT * FROM Chromosome WHERE bits=?', 'r', parameters=[str(solution.best_generation.chromosomes[i].bits)])
      if not chromo:
        db.execute('INSERT INTO Chromosome(bits) VALUES(?)', 'c', parameters=[str(solution.best_generation.chromosomes[i].bits)])
        chromo=db.execute('SELECT * FROM Chromosome WHERE bits=?', 'r', parameters=[str(solution.best_generation.chromosomes[i].bits)])
      chromosomes.append(chromo)
    
    problem_row=db.execute('SELECT * FROM Problem WHERE name=? and target=?', 'r', parameters=[solution.problem['NAME'], str(solution.problem['TARGET'])])
    if not problem_row:
      db.execute('INSERT INTO Problem(name, description, target) VALUES(?, ?, ?)', 'c', parameters=[solution.problem['NAME'], solution.problem['DESCRIPTION'], str(solution.problem['TARGET'])])
      problem_row=db.execute('SELECT * FROM Problem WHERE name=? and target=?', 'r', parameters=[solution.problem['NAME'], str(solution.problem['TARGET'])])

    solution.problem['ID']=int(problem_row[2])    
    prv_best_fitness_score=0
    generation=db.execute('SELECT * FROM Solution WHERE Problem=?', 'r', parameters=[solution.problem['ID']])
    if generation:
      for i in range(len(generation)): prv_best_fitness_score+=generation[i][2]
    
    if solution.best_generation.fitness_score>prv_best_fitness_score:
        solution.best_fitness_score=solution.best_generation.fitness_score
        db.execute('DELETE FROM Solution WHERE Problem=?', 'd', parameters=[solution.problem['ID']])
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
        db.bulk_execute(
          'INSERT INTO Solution(Problem, Chromosome, fitness_score, sequence, solution) VALUES(?, ?, ?, ?, ?) ', 'c', tuples=tuples)
    else:
        solution.best_fitness_score=prv_best_fitness_score

