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

if __name__ == "__main__":
    population_size = 20
    population = [create_chromosome() for _ in range(population_size)]

