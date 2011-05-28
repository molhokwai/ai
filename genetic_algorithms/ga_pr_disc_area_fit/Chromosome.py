#!/usr/bin/python
import math
import base

class Chromosome(base.Chromosome):
  
  def __init__(self, genes, target, bits):
    self.bits=bits
    self.genes=genes
    self.target=target


  @property
  def solution(self):
    if self._solution is None:
      try : self._solution=math.fabs(eval(self.sequence))
      except Exception, ex: return 0
    return self._solution

  @property
  def fitness_score(self):
    if self.target==self.solution: return 1
    return 1/(float(self.target)-float(self.solution))
        
  def decode(self):
    char_bits=self.genes.character_bits
    silent_genes=self.genes.silent
    num_genes=self.genes.numbers
    op_genes_conv=self.genes.operators_conversion
    
    
    seq=''
    prv={'bits':None, 'char':None, '_type':None }
    cur={'bits':None, 'char':None, '_type':None }
    i=0
    while(i<len(self.bits)):
      if char_bits[self.bits[i:i+4]] not in silent_genes:
        for k in cur:
          prv[k]=cur[k]

        cur['bits']=self.bits[i:i+4]
        cur['char']=char_bits[cur['bits']]
        if cur['char'] in num_genes:
          cur['_type']='num'
        else:  
          cur['_type']='op'

        # test:
        #   - no silent gene
        #   - no consecutive types
        if (prv['bits'] not in silent_genes and cur['bits'] not in silent_genes and cur['_type']!=prv['_type']):
          # test ok: append sequence
          seq+=cur['char']+' '
        else:
          # test not ok: do nothing 
          pass
      i+=4

      
    for k in op_genes_conv:
      seq=seq.replace(op_genes_conv[k],k)
    # test:
    #   - num as first char
    if seq[:1] in num_genes:
      # test ok: do nothing
      pass
    else:
      # test not ok: remove
      seq=seq[1:]
      
    # test:
    #   - num as last char
    if seq[len(seq)-2:len(seq)-1] in num_genes:
      # test ok: do nothing
      pass
    else:
      # test not ok: remove
      seq=seq[:len(seq)-2]
    
    return seq

