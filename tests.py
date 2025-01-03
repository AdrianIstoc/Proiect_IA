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
        no_genes=5,  
        population_size=500,
        generations=200,
        F=1.2,
        CR=0.9,
        mini=-5.12,
        maxi=5.12,
        run_mode = "test",
    )

    print("\n")
    print(f"Obtained Result: {test_chromo.genes}, Obtained Fitness: {test_chromo.fitness}")

    chromo = Chromosome(no_genes=5,
                        genes=np.array([-0.01415396, -0.01852149, -0.01292912,  0.00729068,  0.00371603]), run_mode="test")
    chromo.compute_fitness()
    print(f"Rezultat asteptat: {chromo.genes}, Fitness așteptat: {chromo.fitness} (aproximativ in (0.1, 0.8))")