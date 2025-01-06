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
            # In modul de test algorimul are o complexitate de O(G) unde G este numarul de
            # gene pe care le adunam, in cod notat ca no_genes. 
            #
            # In modul de test Genes va fi mereu un array
            #
            # Nu se face nici o optimizare bazata pe calitatea datelor prin urmare
            # algortimul va avea urmatoarele complexitati:
            #   - O(G) - in cel mai rau caz
            #   - Omega(G) -  in cel mai bun caz
            #   - Teta(G) - in cazul normal
            #
            # G = no_genes

            n = self.no_genes
            A = 10
            omega = 2 * np.pi
            self.fitness = n * A + np.sum(self.genes**2 - A * np.cos(omega * self.genes))
        else:
            # In modul de dev algorimul are o complexitate de O(G^2) unde G este numarul de
            # gene parcurse, in cod notat ca no_genes. 
            #
            # In modul de dev Genes va fi mereu un matrice patratica de marimea no_genes x no_genes
            #
            # Cea mai complexa structura din algoritm este parcurgerea de gene, in cadrul aceste parcurgeri se afla si o bucla
            # in care se verifica vecinii unui element din matrice insa aceasta bucla are mere
            # doar 4 iteratii prin urmare parcurgerea de gene va avea o complexitate de O(G * G * 4) = O(G^2)
            #
            # Deoarece buclele de calcul pentru missing_biomes si diversity_penalty au mereu 6 iteratii (numarul de tipuri de teren)
            # acestea ar fi doar O(6) deci le putem neglija in complexitatea finala
            # 
            # In cod nu se fac optimizari in plus bazate pe calitatea datelor parcurse.
            #
            # Astfel algortimul va avea urmatoarele complexitati:
            #   - O(G^2) - in cel mai rau caz
            #   - Omega(G^2) -  in cel mai bun caz
            #   - Teta(G^2) - in cazul normal
            #
            # G = no_genes
            self.genes = np.clip(self.genes, self.min, self.max).astype(int)
            genes = self.genes
            fitness = 0
            diversity_penalty = 0
            local_rule_penalty = 0
            local_rule_bonus = 0
            biomes = np.zeros(self.max + 1)
            
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