import random
import string
import numpy as np

class Chromosome:
    def __init__(self, no_genes: int, genes=None, fitness: float = 0.0, 
                 min: float = 0, max: float = 5, run_mode: string = "dev"):
        self.no_genes = no_genes
        self.min = min
        self.max = max
        self.fitness = fitness
        self.genes = genes

        if(run_mode not in ["dev", "test"]):
            raise ValueError("Mod de run invalid")
        
        self.run_mode = run_mode

        if self.genes is None:
            if self.run_mode == "test": 
                self.genes = np.array([random.uniform(min, max) for _ in range(no_genes)])
            else: 
                self.genes = np.random.randint(low=min, high=max + 1, size=(no_genes, no_genes))
        else:
            self.genes = genes

    def __copy__(self):
        return Chromosome(self.no_genes, self.genes.copy(), self.fitness, self.min, self.max, self.run_mode)

    def compute_fitness(self):
        if self.run_mode == "test":  
            n = self.no_genes
            A = 10
            omega = 2 * np.pi
            self.fitness = n * A + np.sum(self.genes**2 - A * np.cos(omega * self.genes))
        else: 
            self.genes = np.clip(self.genes, 0, 5).astype(int)
            
            if self.genes.ndim == 1:
                side_length = int(np.sqrt(len(self.genes)))
                genes_2d = self.genes[:side_length**2].reshape(side_length, side_length)
            else:
                genes_2d = self.genes

            fitness = 0
            diversity_penalty = 0
            local_rule_penalty = 0  
            counts = np.zeros(6)  
            
            rows, cols = genes_2d.shape
            for i in range(rows):
                for j in range(cols):
                    current_value = genes_2d[i, j]
                    counts[current_value] += 1

                    if j + 1 < cols and genes_2d[i, j + 1] == current_value:
                        fitness += 2

                    if i + 1 < rows and genes_2d[i + 1, j] == current_value:
                        fitness += 2

                    # Regula 1: Beach  trebuie să fie lângă Water
                    if current_value == 1:  
                        if not any(genes_2d[i + di, j + dj] == 0 for di in [-1, 0, 1] if 0 <= i + di < rows for dj in [-1, 0, 1] if 0 <= j + dj < cols):
                            local_rule_penalty += 10  

                    # Regula 2: Mountain trebuie să fie lângă Forest
                    if current_value == 5:  # Mountain
                        if not any(genes_2d[i + di, j + dj] == 4 for di in [-1, 0, 1] if 0 <= i + di < rows for dj in [-1, 0, 1] if 0 <= j + dj < cols):
                            local_rule_penalty += 10  

            # Penalizare pentru absența unui biome
            missing_biomes = sum(1 for count in counts if count == 0)
            diversity_penalty += missing_biomes * 100  

            # Penalizăm dominarea unui biome
            total_cells = rows * cols
            for count in counts:
                proportion = count / total_cells
                if proportion > 0.30:  
                    diversity_penalty += (proportion - 0.30) * 1000  

            # Penalizăm concentrațiile mari ale unui singur biome
            for count in counts:
                proportion = count / total_cells
                diversity_penalty += proportion ** 2 

            # Fitness combinat: favorizăm coerența locală, diversitatea globală și respectarea regulilor
            self.fitness = -fitness + diversity_penalty + local_rule_penalty


