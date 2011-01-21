#!/usr/bin/python
import math

class Chromosome():
  _sequence=None
  _solution=None
  _fitness_score=None

  bits=None
  genes=None
  target=None
  

  def __init__(self, genes, target, bits):
    self.bits=bits
    self.genes=genes
    self.target=target


  @property
  def sequence(self):
    """ Returns the operation sequence, result  of decoding"""
    if self._sequence is None:
      self._sequence=self.decode()
    return self._sequence


  @property
  def solution(self):
    """ To return the solution, result of execution of the sequence"""
    pass
    

  @property
  def fitness_score(self):
    """ To return The fitness score"""
    pass
            

  def decode(self):
    """To decode chromosome bits into operation sequence
        - gets genes details: character bits, silent genes, number genes, operation genes...
        - executes and returns the build sequence
        
        Returns the build sequence
    """
    char_bits=self.genes.character_bits
    silent_genes=self.genes.silent
    num_genes=self.genes.numbers
    op_genes_conv=self.genes.operators_conversion
        
    return self.build_sequence()


  def build_sequence(self):
    """To Build the operation sequence with validation

        Returns the build sequence
    """

    seq=''
    prv={'bits':None, 'char':None, '_type':None }
    cur={'bits':None, 'char':None, '_type':None }
    return seq


  def __repr__(self):
    s=' \nCHROMOSOME'
    s+=' \n----------'
    s+=' \nTarget \t: \t%s' % str(self.target)
    s+=' \nBits \t: \t%s' % str(self.bits)
    s+=' \nSequence \t: \t%s' % str(self.sequence)
    s+=' \nSolution \t: \t%s' % str(self.solution)
    s+=' \nFitness score \t: \t%s' % str(self.fitness_score)
    s+=' \n'
    return s
    
