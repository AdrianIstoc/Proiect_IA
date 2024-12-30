from typing import List
from chromosome import Chromosome
import random

class Selection:
    def tournament(population: List[Chromosome]) -> Chromosome:
        first = random.choice(population)
        second = random.choice(population)
        return first.__copy__() if first.fitness > second.fitness else second.__copy__()
    
    def getBest(population: List[Chromosome]) -> Chromosome:
        return max(population, key=lambda chr: chr.fitness).__copy__()
    
class Crossover:
    def arithmetic(mama: Chromosome, papa: Chromosome, rate: float) -> Chromosome:
        if random.random() < rate:
            child = mama.__copy__()
            for i in range(child.nrGenes):
                a = random.random()
                child.genes[i] = a*mama.genes[i] + (1-a)*papa.genes[i]
            return child
        return mama.__copy__()
    
class Mutation:
    def reset(child: Chromosome, rate: float):
        for i in range(child.nrGenes):
            if random.random() < rate:
                child.genes[i] = random.uniform(child.min[i], child.max[i])

                