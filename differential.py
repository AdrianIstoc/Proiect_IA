from typing import List
from chromosome import Chromosome
import random
import numpy as np

class Selection:
    @staticmethod
    def tournament(first: Chromosome, second: Chromosome) -> Chromosome:
        return first.__copy__() if first.fitness < second.fitness else second.__copy__()

    @staticmethod
    def get_best(population: List[Chromosome], method) -> Chromosome:
        return method(population, key=lambda chr: chr.fitness).__copy__()

class Crossover:
    @staticmethod
    def binomial(mama: Chromosome, papa: Chromosome, CR: float) -> Chromosome:
        k = random.randint(0, mama.no_genes - 1)
        child = np.zeros_like(mama.genes)
        for i in range(mama.no_genes):
            if random.random() < CR or i == k:
                child[i] = mama.genes[i]
            else:
                child[i] = papa.genes[i]

        return Chromosome(no_genes=mama.no_genes, genes=child,
                          min=mama.min, max=mama.max, run_mode=papa.run_mode)

class Mutation:
    @staticmethod
    def self_referential(F: float, population: List[Chromosome], i: int) -> Chromosome:
        indices = list(range(len(population)))
        indices.remove(i)
        r1_i, r2_i, r3_i = random.sample(indices, 3)
        r1, r2, r3 = population[r1_i], population[r2_i], population[r3_i]

        donor = (r1.genes +
                 F * (r2.genes - r3.genes))
        
        original = population[i]

        return Chromosome(no_genes=original.no_genes,
                          genes=donor, min=original.min, max=original.max, run_mode=original.run_mode)

    @staticmethod
    def normal_mutation(MR, population: list[Chromosome]):
        mutation_mask = np.random.rand(5) < MR 
        mutations = np.random.uniform(-5.12, 5.12, (5))
        original = population[0]
        donor = np.where(mutation_mask, mutations, original.genes)
        return Chromosome(no_genes=original.no_genes,
                          genes=donor, min=original.min, 
                          max=original.max, run_mode=original.run_mode)
    

def create_chromosome(no_genes: int = 10, min_val: int = 0, max_val: int = 5, run_mode = "dev"):
    return Chromosome(no_genes=no_genes, min=min_val, max=max_val, run_mode=run_mode)

def diferential_evolution(no_genes = 10, population_size = 500, generations = 1000,
                          F = 1.0, CR=1.0, mini = 0, maxi = 5, run_mode = "dev"):
    population = [create_chromosome(no_genes, mini, maxi, run_mode=run_mode) for _ in range(population_size)]
    for chromo in population:
        chromo.compute_fitness()

    best_chromo = Selection.get_best(population, min)

    for gen in range(generations):
        new_population = []

        for i, chromo in enumerate(population):
            F_dynamic = random.uniform(min(F/1000, F - 0.5), max(1.9, F + 0.5))
            CR_dynamic = random.uniform(min(0.65, CR - 0.2), max(0.9, CR + 0.2))

            #donor = Mutation.normal_mutation(0.2, population)
            donor = Mutation.self_referential(F_dynamic, population, i)

            trial = Crossover.binomial(chromo, donor, CR_dynamic)
            trial.compute_fitness()

            winner = Selection.tournament(trial, chromo)
            new_population.append(winner)

        population = new_population

        best_candidate = Selection.get_best(population, min)
        if best_candidate.fitness < best_chromo.fitness:
            best_chromo = best_candidate

        print(f"Generation {gen + 1}: Best Fitness = {best_chromo.fitness}")

    print("\n------------------ Results ------------------")
    print(f"Final Result: \n{np.round(best_chromo.genes).astype(int) if best_chromo.genes.ndim > 1 else best_chromo.genes}\nFitness: {best_chromo.fitness}")
    return best_chromo