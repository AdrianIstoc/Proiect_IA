from chromosome import Chromosome

biomes = {
    0, # Apa 
    1, # Plaja
    2, # Desert
    3, # Campie
    4, # Padure
    5, # Munte
}

def create_chromosome(no_genes: int = 10, min:int = 0, max:int = 5):
    return Chromosome(no_genes=no_genes, min=min, max=max)

def compute_fitness(chromosome: Chromosome) -> float:
    genes = chromosome.genes
    n = chromosome.no_genes
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
                        fitness +=0.5
                    
                    # Regula 9: Deșert lângă plajă sau câmpie
                    if current == 2 and (neighbor == 1 or neighbor == 3):
                        fitness +=0.3

    return fitness


if __name__ == "__main__":
    population_size = 20
    population = [create_chromosome() for _ in range(population_size)]

