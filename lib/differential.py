from typing import List
from lib.chromosome import Chromosome
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
        original = population[0]
        mutation_mask = np.random.rand(original.no_genes**2) < MR 
        mutations = np.random.uniform(original.min, original.max, (original.no_genes**2))
        donor = np.where(mutation_mask, mutations, original.genes)
        return Chromosome(no_genes=original.no_genes,
                          genes=donor, min=original.min, 
                          max=original.max, run_mode=original.run_mode)
    

def create_chromosome(no_genes: int = 10, min_val: float = 0, max_val: float = 5, run_mode = "dev"):
    return Chromosome(no_genes=no_genes, min=min_val, max=max_val, run_mode=run_mode)

def diferential_evolution(no_genes = 10, population_size = 500, generations = 1000, 
                          F = 1.0, CR=1.0, mini = 0, maxi = 5, run_mode = "dev"):
    """
    O Implementare a algoritmului de evolutie diferentiala, in care factor de mutatie 
    si rata de incrucisare pot varia de la valorile initiale

    Return
    ---------
    Returneaza cromozomul cu cel mai bun fitness gasit.
    
    Parameters
    ----------
    no_genes : int, default 10
        Indică mărimea hărții pe care dorim să o generam, pentru valoarea 10 vom avea o harta de 10x10;
    population_size : int, default 500
        Numărul de cromozomi care vor participa în procesul de evoluție;
    generations : int, default 1000
        Numărul de generații pe care le va efectua algoritmul;
    F : float, default 1.0
        Factorul de mutație, folosit pentru a specifica cat de volatile pot fi mutațiile, aceasta variaza cu += 0.5
    CR : float, default 0.9
        Proporția în care un cromozom moștenește gene de la cromozomul mutant, aceasta variaza cu += 0.2
    mini : float, default 5
        Limita inferioară a valorilor din gene
    maxi : float, default 0
        Limita superioară a valorilor din gene
    run_mode : string, default "dev"
        Poate fi "dev" sau "test".
        - "test" va rula algoritmul folosind o functie de fitness pentru a 
        vedea mai usor functionalitatea algoritmului.
        - "dev" va rula algoritmul in mod normal pentru generarea unei harti.
    """
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