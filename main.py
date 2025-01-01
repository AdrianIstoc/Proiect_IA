import numpy as np
from chromosome import Chromosome
from differential import Crossover, Mutation, Selection
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


biomes = {
    "blue": 0,       # Apa 
    "yellow": 1,     # Plaja
    "orange": 2,     # Desert
    "lightgreen": 3, # Campie
    "green": 4,      # Padure
    "grey": 5,       # Munte
}

def create_chromosome(no_genes: int = 10, min:int = 0, max:int = 5):
    return Chromosome(no_genes=no_genes, min=min, max=max)

def diferential_evolution(no_genes = 10, population_size = 50, 
                          generations = 1000, F = 1.2, CR = 0.7):
    
    # Generăm populația inițială
    population = [create_chromosome(no_genes) for _ in range(population_size)]

    for chromo in population:
        chromo.compute_fitness()
    for gen in range(generations):
        new_population = []

        for i, chromo in enumerate(population):
            donor: Chromosome = Mutation.self_referential(F, population, i)
            trial: Chromosome = Crossover.binomial(chromo, donor, CR)
            trial.compute_fitness()

            new_population.append(Selection.tournament(trial, chromo))

        population = new_population
        best = max(population, key=lambda x: x.fitness)
        print(f"Generația {gen + 1}: Cel mai bun Fitness = {best.fitness}")

    best_chromo = max(population, key=lambda x: x.fitness)
    print("------------------ Rezultate ------------------")
    print("\nCea mai bună mapă generată:")
    print(best_chromo.genes)

    print("Fitness final:", best_chromo.fitness)

    return best_chromo

def test_fitness(cmap):
    test_chromo = create_chromosome()
    
    with open('ideal.txt', 'r') as f:
        test_mat = [[int(num) for num in line.split(' ')] for line in f]

    test_chromo.genes = np.array(test_mat)
    
    print(test_chromo.genes)
    test_chromo.compute_fitness()

    plt.imshow(test_chromo.genes, cmap=cmap, interpolation='nearest')
    print(f"Test Mat Fitness: {test_chromo.fitness}")
    plt.show()

if __name__ == "__main__":
    # Creează lista de culori pe baza ordinii valorilor
    colors = [color for color, _ in sorted(biomes.items(), key=lambda item: item[1])]
    cmap = ListedColormap(colors)

    best_chromo = diferential_evolution(
        no_genes=10,
        population_size=35,
        generations=200,
        F = 1.3,
        CR = 0.8,
    )

    # Desenează matricea
    plt.imshow(best_chromo.genes, cmap=cmap, interpolation='nearest')
    plt.show()

    # Testeaza functia de fitness pe o harta considerata buna 
    test_fitness(cmap)