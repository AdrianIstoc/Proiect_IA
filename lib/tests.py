from matplotlib import pyplot as plt
import numpy as np
import timeit

from lib.chromosome import Chromosome
from lib.differential import create_chromosome, diferential_evolution

def test_ideal_mat_fitness(cmap):
    test_chromo = create_chromosome()

    with open('inputs/ideal.txt', 'r') as f:
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


############## TESTE EP ################

def test_fitness_best():
    test_chromo = create_chromosome()

    with open('inputs/best.txt', 'r') as f:
        test_mat = [[int(num) for num in line.split(' ')] for line in f]

    test_chromo.genes = np.array(test_mat)

    execution_time = timeit.timeit(lambda: test_chromo.compute_fitness(),number=1)

    print("\n------------------ Best case ------------------")
    print(f"Tested matrix: \n{test_chromo.genes}\n Fitness: {test_chromo.fitness}")
    print(f"Time to execute: {execution_time:f}\n")


def test_fitness_worst():
    test_chromo = create_chromosome()

    with open('inputs/worst.txt', 'r') as f:
        test_mat = [[int(num) for num in line.split(' ')] for line in f]

    test_chromo.genes = np.array(test_mat)

    execution_time = timeit.timeit(lambda: test_chromo.compute_fitness(),number=1)

    print("\n------------------ Worst case ------------------")
    print(f"Tested matrix: \n{test_chromo.genes}\n Fitness: {test_chromo.fitness}")
    print(f"Time to execute: {execution_time:f}\n")


def test_fitness_average():
    test_chromo = create_chromosome()

    execution_time = timeit.timeit(lambda: test_chromo.compute_fitness(),number=1)
    
    print("\n------------------ Average case ------------------")
    print(f"Tested matrix: \n{test_chromo.genes}\n Fitness: {test_chromo.fitness}")
    print(f"Time to execute: {execution_time:f}\n")