from chromosome import Chromosome
from differential import Crossover, Mutation, Selection
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


biomes = {
    "blue": 0, # Apa 
    "yellow":  1, # Plaja
    "orange": 2, # Desert
    "lightgreen": 3, # Campie
    "green": 4, # Padure
    "grey": 5, # Munte
}

def create_chromosome(no_genes: int = 20, min:int = 0, max:int = 5):
    return Chromosome(no_genes=no_genes, min=min, max=max)

if __name__ == "__main__":
    population_size = 20
    generations = 50
    population = [create_chromosome() for _ in range(population_size)]
    F = 0.7
    CR = 1.0

    for individual in population:
        individual.compute_fitness()
    
    for gen in range(generations):
        new_population = []

        for i, chromo in enumerate(population):
             donor : Chromosome = Mutation.self_referential(F, population, i)
             trial : Chromosome = Crossover.binomial(chromo, donor, CR)

             trial.compute_fitness()

             new_population.append(Selection.tournament(trial, chromo))

        population = new_population
        best = max(population, key=lambda x: x.fitness)
        print(f"Generatia {gen + 1}: Cel mai bun Fitness = {best.fitness}")
    

    best_chromo = max(population, key=lambda x: x.fitness)
    print("------------------ Rezultate ------------------")
    print("\nCea mai bună mapă generată:")
    print(best_chromo.genes)
    print("Fitness final:", best_chromo.fitness)

    # Creează lista de culori pe baza ordinii valorilor
    colors = [color for color, value in sorted(biomes.items(), key=lambda item: item[1])]

    # Creează colormap-ul
    cmap = ListedColormap(colors)

    plt.figure(figsize=(best_chromo.no_genes, best_chromo.no_genes))

    # Desenează matricea
    plt.imshow(best_chromo.genes, cmap=cmap, interpolation='nearest')

    # Adaugă o bară de culori pentru referință
    colorbar = plt.colorbar(ticks=range(6))
    colorbar.ax.set_yticklabels([str(i) for i in range(6)])

    plt.show()