from typing import List
from chromosome import Chromosome
import random
import numpy as np

class Selection:
    def tournament(first: Chromosome, second:Chromosome) -> Chromosome:

        return first.__copy__() if first.fitness > second.fitness else second.__copy__()
    
    # def get_best(population: List[Chromosome]) -> Chromosome:
    #     return max(population, key=lambda chr: chr.fitness).__copy__()
    
class Crossover:
    def binomial(mama: Chromosome, papa: Chromosome, CR: float) -> Chromosome:
        k = random.randint(0, mama.no_genes)
        child = np.zeros((mama.no_genes, mama.no_genes))
        for i in range(mama.no_genes):
            if random.random() < CR or i==k:
                child[i] = mama.genes[i]
            else:
                child[i] = papa.genes[i]

        return Chromosome(no_genes = mama.no_genes, genes = child, min = mama.min, max = mama.max) 
               
class Mutation:
    def self_referential(F:float, population: List[Chromosome], i:int) -> Chromosome:
        r1,r2,r3 = random.sample(range(0, len(population)), 3)
        while i in [r1,r2,r3]:
            r1,r2,r3 = random.sample(range(0, len(population)), 3)
        
        donor = np.abs(np.round(
            population[r1].genes + F * (population[r2].genes - population[r3].genes)
            ))
        original = population[i]
        donor = np.clip(donor, original.min, original.max)

        return Chromosome(no_genes = original.no_genes, 
                          genes = donor, min = original.min, max = original.max)
                