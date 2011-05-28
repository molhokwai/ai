#!/usr/bin/python
"""
  Application of example from: http://www.ai-junkie.com/ga/intro/gat3.html
"""
import config
import settings

from Genes import Genes
from Chromosome import Chromosome
from base.Main import Main
from base.Solution import Solution
from base.Selection import Selection


def main():
  return Main(Genes, Chromosome, Selection, Solution, config, settings)

