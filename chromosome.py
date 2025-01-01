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

                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    
                    if 0 <= ni < self.no_genes and 0 <= nj < self.no_genes:
                        neighbor = self.genes[ni][nj]

                        # Regula 1: Valori egale apropiate
                        if current == neighbor:
                            fitness += 5
                        
                        # Regula 2: Apa lângă orice biome
                        if current == 0 or neighbor == 0:
                            fitness += 1
                        
                        # Regula 3: Munte lângă pădure
                        if (current == 5 and neighbor == 4) or (current == 4 and neighbor == 5):
                            fitness += 0.7
                        
                        # Regula 4: Pădure lângă câmpie
                        if (current == 4 and neighbor == 3) or (current == 3 and neighbor == 4):
                            fitness += 1
                        
                        # Regula 5: Plajă lângă apă
                        if current == 1 and neighbor != 0:
                            fitness -= 2 

                        # Regula 6: Apă în deșert
                        if current == 2 and neighbor == 0:
                            fitness -= 1

                        # Regula 7: Câmpie lângă plajă
                        if current == 3 and neighbor == 1:
                            fitness += 1

                        # Regula 8: Deșert lângă deșert
                        if current == 2 and neighbor == 2:
                            fitness += 4
                        
                        # Regula 9: Deșert lângă plajă sau câmpie
                        if current == 2 and (neighbor == 1 or neighbor == 3):
                            fitness += 1
                        
                        

        self.fitness = fitness
        return self.fitness