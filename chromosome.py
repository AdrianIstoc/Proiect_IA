import random
import numpy as np
from scipy.ndimage import label

class Chromosome:
    def __init__(self, no_genes: int, genes = None, fitness: float = 0.0, min: float = 0, max: float = 5):
        self.no_genes = no_genes
        self.min = min
        self.max = max
        self.fitness = fitness

        if no_genes == 1 and genes is None:
            genes = random.uniform(min, max)

        if genes is None:
            self.genes = np.random.randint(low=min, high=max + 1, size=(no_genes, no_genes))
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
        
    def compute_fitness(self):
        if(self.no_genes == 1):
            self.fitness = -abs(self.genes**5 - 5*self.genes + 5)
        else:
            genes = self.genes
            no_genes = self.no_genes
            
            # 1. Contiguous Regions (Homogeneity)
            labeled, num_features = label(genes)
            region_sizes = np.bincount(labeled.ravel())[1:]  # Skip the background (0)
            homogeneity_score = np.sum(region_sizes ** 1.2) / (no_genes ** 2)  # Reward larger regions

            # 2. Penalize Over-Dominance
            value_counts = np.bincount(genes.astype(int).ravel(), minlength=self.max + 1)
            max_value_ratio = np.max(value_counts) / (no_genes ** 2)
            dominance_penalty = 50 * max(0, max_value_ratio - 0.3)  # Penalize dominance > 30%

            # 3. Smooth Transitions
            transition_penalty = 0
            for i in range(no_genes - 1):
                for j in range(no_genes - 1):
                    transition_penalty += abs(genes[i, j] - genes[i + 1, j])  # Vertical
                    transition_penalty += abs(genes[i, j] - genes[i, j + 1])  # Horizontal

            smoothness_score = max(0, 100 - (transition_penalty / (no_genes * 2)))  # Scale transition penalty

            # 4. Diversity of Values
            unique_values = len(np.unique(genes))
            diversity_score = (unique_values - 1) / (self.max - self.min) * 100

            # Final Fitness Calculation
            fitness_score = (homogeneity_score + smoothness_score + diversity_score) / 3
            fitness_score -= dominance_penalty
            fitness_score = max(0, fitness_score)  # Ensure non-negative fitness

            self.fitness = fitness_score
            return self.fitness
