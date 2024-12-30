from typing import List
import random

class Chromosome:

    __rand = random.Random()

    def __init__(self, nrGenes: int, genes: List[float], min: List[float], max: List[float], fitness: float):
        self.nrGenes = nrGenes
        self.genes = genes
        self.min = min
        self.max = max
        self.fitness = fitness

        for i in range(self.nrGenes):
            self.genes[i] = self.min[i] + (self.max[i]-self.min[i]) * Chromosome.__rand.random() # intre 0 si 1
    
    def __copy__(self):
        return Chromosome(self.nrGenes, self.genes, self.min, self.max, self.fitness)