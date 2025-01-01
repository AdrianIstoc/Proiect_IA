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

    def compute_fitness(self) -> float:
        fitness = 0.0

        directions = [
            (-1, 0),   # Sus 
            (1, 0),    # Jos 
            (0, -1),   # Stânga 
            (0, 1),    # Dreapta 
            (-1, -1),  # Sus-Stânga 
            (-1, 1),   # Sus-Dreapta 
            (1, -1),   # Jos-Stânga 
            (1, 1),    # Jos-Dreapta 
        ]
        
        for i in range(self.no_genes):
            for j in range(self.no_genes):
                current = self.genes[i][j]

                if current == 0:
                    fitness += 2.5
                elif current == 3:
                    fitness += 2.3
                else:
                    fitness -= 3.1

                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    
                    if 0 <= ni < self.no_genes and 0 <= nj < self.no_genes:
                        neighbor = self.genes[ni][nj]

                        if current == neighbor:
                            fitness += 1
                        

        self.fitness = fitness
        return self.fitness