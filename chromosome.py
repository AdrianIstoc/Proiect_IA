import numpy as np

class Chromosome:
    def __init__(self, no_genes: int, genes:np.ndarray[int] = None, fitness: float = 0.0, min : int = 0, max: int = 5):
        self.no_genes = no_genes
        self.min = min
        self.max = max
        self.fitness = fitness

        if genes is None :
            self.genes = np.random.randint(low = min, high = max+1, size = (no_genes, no_genes))
        else:
            self.genes = genes

    def __copy__(self):
        return Chromosome(self.no_genes, self.genes, self.fitness, self.min, self.max)
    
    def copy_from(self, other):
        self.no_genes = other.no_genes
        self.genes = other.genes
        self.min = other.min
        self.max = other.max
        self.fitness = other.fitness