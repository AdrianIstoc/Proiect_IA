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
        """
        Functia determina vloare de fitness a unui Chromozom

        
        Poate fi rulata in 2 moduri:
            * \"dev\" - Modul normal de utilizare.
            * \"test\" - In acest mod functia va calcula fitness-ul pentru functia Rastrigin.
        
        Valoare de fitness calculata va fi salvata in Chromozom.

        O valoare mai mica este o valoare mai buna 
        """
        if self.run_mode == "test":  
            n = self.no_genes
            A = 10
            omega = 2 * np.pi
            self.fitness = n * A + np.sum(self.genes**2 - A * np.cos(omega * self.genes))
        else: 
            self.genes = np.clip(self.genes, 0, 5).astype(int)

            genes = self.genes

            fitness = 0
            diversity_penalty = 0
            local_rule_penalty = 0
            local_rule_bonus = 0
            biomes = np.zeros(6)
            
            rows, cols = genes.shape

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for i in range(rows):
                for j in range(cols):
                    current_value = genes[i, j]
                    biomes[current_value] += 1

                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols:
                            neighbor_value = genes[ni, nj]
                            
                            # valori similare apropiate
                            if current_value == neighbor_value:
                                fitness += 7

                            # Regula 1: DA Plaja lângă Apa
                            if current_value == 1: 
                                if neighbor_value == 0:
                                    local_rule_bonus += 1
                                else:
                                    local_rule_penalty += 16

                            # Regula 2: NU Desert lângă Apa
                            if current_value == 2:
                                if neighbor_value == 0: 
                                    local_rule_penalty += 30
                                else:
                                    local_rule_bonus += 2
                            
                            # Regula 3: NU Desert lângă Padure
                            if current_value == 2:
                                if neighbor_value == 4: 
                                    local_rule_penalty += 15
                                else:
                                    local_rule_bonus += 2

                             # Regula 4: Da Campie lângă Padure
                            if current_value == 3:
                                if neighbor_value == 4:
                                    local_rule_bonus += 5
                                else:
                                    local_rule_penalty += 20

                            # Regula 5: Da Campie lângă Desert
                            if current_value == 3:
                                if neighbor_value == 2:
                                    local_rule_bonus += 4
                                else:
                                    local_rule_penalty += 20

                            # Regula 6: DA Munte lângă Padure
                            if current_value == 5:
                                if neighbor_value == 4:  
                                    local_rule_bonus += 3
                                else:
                                    local_rule_penalty += 10

            missing_biomes = sum(1 for biome in biomes if biome == 0)
            diversity_penalty += missing_biomes * 100

            total_cells = rows * cols
            for biome in biomes:
                proportion = biome / total_cells
                if proportion > 0.3:
                    diversity_penalty += (proportion - 0.3) * 3500

            self.fitness = (
                    -(fitness + local_rule_bonus) 
                    + diversity_penalty 
                    + local_rule_penalty
                )