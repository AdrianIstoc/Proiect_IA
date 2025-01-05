import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from differential import diferential_evolution
from tests import *

biomes = {
    "blue": 0,       # Apa 
    "yellow": 1,     # Plaja
    "orange": 2,     # Desert
    "lightgreen": 3, # Campie
    "green": 4,      # Padure
    "grey": 5,       # Munte
}

if __name__ == "__main__":
    # Creează lista de culori pe baza ordinii valorilor
    colors = [color for color, _ in sorted(biomes.items(), key=lambda item: item[1])]
    cmap = ListedColormap(colors)

    best_chromo = diferential_evolution(
        no_genes = 10,
        population_size = 200,
        generations = 300,
        F = 1.2,
        CR = 0.9,
        mini = 0,
        maxi = 5,
    )

    # Desenează matricea
    plt.imshow(best_chromo.genes, cmap=cmap, interpolation='nearest')
    plt.show()

    # Testeaza functia de fitness pe o harta considerata buna 
    test_ideal_mat_fitness(cmap)
    test_rnd_mat_fitness(cmap)
    test_dif_func()

    test_fitness_best()
    test_fitness_worst()
    test_fitness_average()