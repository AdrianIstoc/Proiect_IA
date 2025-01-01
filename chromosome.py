import numpy as np

class Chromosome:
    def __init__(self, no_genes: int, genes: np.ndarray[int] = None, fitness: float = 0.0, min: int = 0, max: int = 5):
        self.no_genes = no_genes
        self.min = min
        self.max = max
        self.fitness = fitness

        if genes is None:
            self.genes = np.random.randint(low=min, high=max + 1, size=(no_genes, no_genes))
        else:
            self.genes = genes

    def __copy__(self):
        return Chromosome(self.no_genes, self.genes.copy(), self.fitness, self.min, self.max)

    def copy_from(self, other):
        self.no_genes = other.no_genes
        self.genes = other.genes.copy()
        self.min = other.min
        self.max = other.max
        self.fitness = other.fitness

    import numpy as np

class Chromosome:
    def __init__(self, no_genes: int, genes: np.ndarray[int] = None, fitness: float = 0.0, min: int = 0, max: int = 5):
        self.no_genes = no_genes
        self.min = min
        self.max = max
        self.fitness = fitness

        if genes is None:
            self.genes = np.random.randint(low=min, high=max + 1, size=(no_genes, no_genes))
        else:
            self.genes = genes

    def __copy__(self):
        return Chromosome(self.no_genes, self.genes.copy(), self.fitness, self.min, self.max)

    def copy_from(self, other):
        self.no_genes = other.no_genes
        self.genes = other.genes.copy()
        self.min = other.min
        self.max = other.max
        self.fitness = other.fitness

    def compute_fitness(self):
        fitness = 0.0

        # Direcțiile vecinătății (sus, jos, stânga, dreapta + diagonale)
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

        # Verifică vecinii direcți
        for i in range(self.no_genes):
            for j in range(self.no_genes):
                current = self.genes[i][j]
                neighbor_counts = {k: 0 for k in range(6)}  # Contor pentru fiecare tip de vecin

                # Verifică vecinii direcți
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.no_genes and 0 <= nj < self.no_genes:
                        neighbor = self.genes[ni][nj]
                        neighbor_counts[neighbor] += 1  # Numără fiecare tip de vecin

                # Condiții pentru fiecare tip de teren
                if current == 0:  # Apă
                    fitness += 10 * neighbor_counts[0]  # Grupuri mari de apă
                    if neighbor_counts[1] > 0:  # Plaja lângă apă
                        fitness += 2  # Favorizează plaja lângă apă
                elif current == 1:  # Plajă
                    if neighbor_counts[0] == 0:  # Plaja fără apă
                        fitness -= 20  # Penalizează dacă nu are vecin apă
                    else:
                        fitness += 5  # Favorizează plaja lângă apă
                elif current == 2:  # Deșert
                    fitness += 5 * neighbor_counts[2]  # Grupuri mari de deșert
                    if neighbor_counts[1] > 0 or neighbor_counts[3] > 0:  # Lângă plajă sau câmpie
                        fitness += 3
                    else:
                        fitness -= 5  # Penalizează dacă nu este lângă plajă/câmpie
                elif current == 3:  # Câmpie
                    if neighbor_counts[1] > 0 or neighbor_counts[4] > 0:  # Lângă plajă sau pădure
                        fitness += 4
                    fitness += neighbor_counts[3]  # Grupuri mari de câmpie
                elif current == 4:  # Pădure
                    if neighbor_counts[3] > 0 or neighbor_counts[5] > 0:  # Lângă câmpie sau munte
                        fitness += 3
                    fitness += neighbor_counts[4]  # Grupuri mari de pădure
                elif current == 5:  # Munte
                    if neighbor_counts[5] > 2:  # Penalizează grupuri mari de munte
                        fitness -= 10
                    else:
                        fitness += 2  # Favorizează muntele izolat

        self.fitness = fitness
        return self.fitness
