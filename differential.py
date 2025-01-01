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
    def arithmetic(mama: Chromosome, papa: Chromosome, rate: float) -> Chromosome:
        k = random.randint(0, mama.no_genes)
        child = np.zeros(mama.no_genes, mama.no_genes)
        for i in range(mama.no_genes):
            if random.random() < rate or i==k:
                child[i] = mama[i]
            else:
                child[i] = papa[i]

        return Chromosome(no_genes = mama.no_genes, genes = child, min = mama.min, max = mama.max) 
               
class Mutation:
    def reset(child: Chromosome, rate: float):
        for i in range(child.nrGenes):
            if random.random() < rate:
                child.genes[i] = random.uniform(child.min[i], child.max[i])

                