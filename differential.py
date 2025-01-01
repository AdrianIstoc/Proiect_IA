from typing import List
from chromosome import Chromosome
import random
import numpy as np

class Selection:
    def tournament(population: List[Chromosome]) -> Chromosome:
        first = random.choice(population)
        second = random.choice(population)
        return first.__copy__() if first.fitness > second.fitness else second.__copy__()
    
    def get_best(population: List[Chromosome]) -> Chromosome:
        return max(population, key=lambda chr: chr.fitness).__copy__()
    
class Crossover:
    def binomial(mama: Chromosome, papa: Chromosome, rate: float) -> Chromosome:
        k = random.randint(0, mama.no_genes)
        child = np.zeros(mama.no_genes, mama.no_genes)
        for i in range(mama.no_genes):
            if random.random() < rate or i==k:
                child[i] = mama[i]
            else:
                child[i] = papa[i]

        return Chromosome(no_genes = mama.no_genes, genes = child, min = mama.min, max = mama.max) 
               
class Mutation:
    def self_referential(child: Chromosome, x: Chromosome):
        F = random.random(0,2)
        for i in range(child.nrGenes):
            r1 = random.randint(0, x.no_genes)
            r2 = random.randint(0, x.no_genes)
            r3 = random.randint(0, x.no_genes)
            child.genes[i] = x.genes[r1] + F *(x.genes[r2] - x.genes[r3])

                