#!/usr/bin/python
"""
  Application of example from: http://www.ai-junkie.com/ga/intro/gat3.html
"""
from base.Selection import Selection
from base.Solution import Solution
import config
import settings

from Genes import Genes
from base.Main import Main


def main():
  return Main(Genes, Selection, Solution, config, settings)

