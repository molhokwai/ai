#!/usr/bin/python
class Genes:

  def __init__(self, chromosome_character_nr=9,
               chromosome_character_bits_nr=4):
    self.chromosome_character_nr=chromosome_character_nr
    self.chromosome_character_bits_nr=chromosome_character_bits_nr
      

  @property
  def chromosome_bits_nr(self):
    return self.chromosome_character_nr * self.chromosome_character_bits_nr

  @property
  def numbers(self):
    """ Number genes for chromosome number of character bits = 4"""
    return {
      '0':         '0000',
      '1':         '0001',
      '2':         '0010',
      '3':         '0011',
      '4':         '0100',
      '5':         '0101',
      '6':         '0110',
      '7':         '0111',
      '8':         '1000',
      '9':         '1001'
    }

  @property
  def operators(self):
    """ Basic algebric opetations for chromosome number of character bits = 4"""
    return {
      '+':         '1010',
      '-':          '1011',
      '*':          '1100',
      '/':          '1101'
    }

  @property
  def operators_conversion(self):
    """ Op genes, with fix for EOF op char eval output """
    return {
      '+':         '100',
      '-':          '101',
      '*':          '102',
      '/':          '103'
    }
    
  @property
  def silent(self):
    """ Silent genes for Basic algebric opetations sequence, for chromosome number of character bits = 4"""
    return {
      '1110':          '1110',
      '1111':          '1111'
    }
    
  @property
  def _all(self):
    """ All non-silent genes """
    genes={}
    for k in self.numbers:
      genes[k]=self.numbers[k]
      
    for k in self.operators:
      genes[self.operators_conversion[k]]=self.operators[k]
      
    for k in self.silent:
      genes[k]=self.silent[k]
    
    return genes
    
  @property
  def character_bits(self):
    """ Chromosome character bits list """
    c_b={}
    for k in self._all:
      c_b[self._all[k]]=k
    return c_b

