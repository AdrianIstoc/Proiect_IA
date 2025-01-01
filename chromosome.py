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
            (-1, 0),   # Sus (Nord)
            (1, 0),    # Jos (Sud)
            (0, -1),   # Stânga (Vest)
            (0, 1),    # Dreapta (Est)
            (-1, -1),  # Sus-Stânga (Nord-Vest)
            (-1, 1),   # Sus-Dreapta (Nord-Est)
            (1, -1),   # Jos-Stânga (Sud-Vest)
            (1, 1),    # Jos-Dreapta (Sud-Est)
        ]

        for i in range(n):
            for j in range(n):
                current = genes[i][j]

                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    
                    if 0 <= ni < n and 0 <= nj < n:
                        neighbor = genes[ni][nj]

                        # Regula 1: Valori egale apropiate
                        if current == neighbor:
                            fitness += 1
                        
                        # Regula 2: Apa lângă orice biome
                        if current == 0 or neighbor == 0:
                            fitness += 0.5
                        
                        # Regula 3: Munte lângă pădure
                        if (current == 5 and neighbor == 4) or (current == 4 and neighbor == 5):
                            fitness += 0.75
                        
                        # Regula 4: Pădure lângă câmpie
                        if (current == 4 and neighbor == 3) or (current == 3 and neighbor == 4):
                            fitness += 0.75
                        
                        # Regula 5: Plajă lângă apă
                        if current == 1 and neighbor != 0:
                            fitness -= 2 

                        # Regula 6: Apă în deșert
                        if current == 2 and neighbor == 0:
                            fitness -= 0.2

                        # Regula 7: Câmpie lângă plajă
                        if current == 3 and neighbor == 1:
                            fitness += 0.4

                        # Regula 8: Deșert lângă deșert
                        if current == 2 and neighbor == 2:
                            fitness += 0.5
                        
                        # Regula 9: Deșert lângă plajă sau câmpie
                        if current == 2 and (neighbor == 1 or neighbor == 3):
                            fitness += 0.3

        self.fitness = fitness