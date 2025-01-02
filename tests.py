from matplotlib import pyplot as plt
import numpy as np

from chromosome import Chromosome
from differential import create_chromosome, diferential_evolution

def test_ideal_mat_fitness(cmap):
    test_chromo = create_chromosome()

    with open('ideal.txt', 'r') as f:
        test_mat = [[int(num) for num in line.split(' ')] for line in f]

    test_chromo.genes = np.array(test_mat)

    print("\n")
    print(test_chromo.genes)
    test_chromo.compute_fitness()

    plt.imshow(test_chromo.genes, cmap=cmap, interpolation='nearest')
    print(f"Ideal Mat Fitness: {test_chromo.fitness}")
    plt.show()

def test_rnd_mat_fitness(cmap):
    test_chromo = create_chromosome()

    print("\n")
    print(test_chromo.genes)
    test_chromo.compute_fitness()

    plt.imshow(test_chromo.genes, cmap=cmap, interpolation='nearest')
    print(f"Random Mat Fitness: {test_chromo.fitness}")
    plt.show()


def test_dif_func():
    test_chromo = diferential_evolution(
        no_genes = 1,
        population_size = 500,
        generations = 50,
        F = 1.2,
        CR = 0.9,
        mini = -5.0,
        maxi = 5.0,
    )

    print("\n")
    print(f"Rezultat  obtinut: {test_chromo.genes:.6f}, Fitness  obtinut: {test_chromo.fitness}")
    chromo = Chromosome(no_genes=1, genes=-1.680494)
    chromo.compute_fitness()
    print(f"Rezultat asteptat: {chromo.genes:.6f}, Fitness așteptat: {chromo.fitness}")