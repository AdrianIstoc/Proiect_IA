from typing import List
from chromosome import Chromosome
import random
import numpy as np

class Selection:
    @staticmethod
    def tournament(first: Chromosome, second:Chromosome) -> Chromosome:
        return first.__copy__() if first.fitness > second.fitness else second.__copy__()
    
    def get_best(population: List[Chromosome], method: min) -> Chromosome:
        return method(population, key=lambda chr: chr.fitness).__copy__()
    
class Crossover:
    @staticmethod
    def binomial(mama: Chromosome, papa: Chromosome, CR: float) -> Chromosome:
        if mama.no_genes == 1:
            child = mama.genes if random.random() < CR else papa.genes
        else:
            k = random.randint(0, mama.no_genes)
            child = np.zeros((mama.no_genes, mama.no_genes))
            for i in range(mama.no_genes):
                if random.random() < CR or i == k:
                    child[i] = mama.genes[i]
                else:
                    child[i] = papa.genes[i]
        
        return Chromosome(no_genes=mama.no_genes, genes=child, 
                          min=mama.min, max=mama.max)
               
class Mutation:
    @staticmethod
    def self_referential(F:float, population: List[Chromosome], i:int) -> Chromosome:
            r1,r2,r3 = random.sample(range(0, len(population)), 3)
            while i in [r1,r2,r3]:
                r1,r2,r3 = random.sample(range(0, len(population)), 3)
            
            donor = ( population[r1].genes +
                      F * (population[r2].genes - population[r3].genes) 
                    )
            
            
            original = population[i]
            donor = np.clip(donor, original.min, original.max)

            return Chromosome(no_genes = original.no_genes, 
                            genes = donor, min = original.min, max = original.max)




def create_chromosome(no_genes: int = 10, min:int = 0, max:int = 5):
    return Chromosome(no_genes=no_genes, min=min, max=max)

def diferential_evolution(no_genes=10, population_size=500, generations=5000, 
                          F=1.0, CR=1.0, mini=0, maxi=5):
    
    population = [create_chromosome(no_genes, mini, maxi) for _ in range(population_size)]
    for chromo in population:
        chromo.compute_fitness()

    best_chromo = Selection.get_best(population, max)
    last_best_fitness = best_chromo.fitness
    stagnant_generations = 0 

    F_init = F
    F_min = 1e-8

    for gen in range(generations):
        new_population = []
        
        F = max(F_min, F_init - (gen/generations))

        # Check stagnation
        if best_chromo.fitness == last_best_fitness:
            stagnant_generations += 1
        else:
            stagnant_generations = 0

        last_best_fitness = best_chromo.fitness

        # More aggressive refresh if stagnation occurs
        if stagnant_generations >= 5:
            refresh_fraction = 0.7  
            refresh_count = int(len(population) * refresh_fraction)
            print(f"Generatia {gen + 1} stagneaza. Inlocuim {refresh_count} chromozomi din populatie.")
            population.sort(key=lambda x: x.fitness)
            for i in range(refresh_count):
                population[i] = create_chromosome(no_genes, mini, maxi)
                population[i].compute_fitness()
            stagnant_generations = 0 

        # Exploration phase (first 1000 generations)

        for i, chromo in enumerate(population):
            donor = Mutation.self_referential(F, population, i)
            trial = Crossover.binomial(chromo, donor, CR)
            trial.compute_fitness()

            winner = Selection.tournament(trial, chromo)
            new_population.append(winner)
       

        population = new_population

        # Maintain the best chromosome
        best_candidate = Selection.get_best(population, max)
        if best_candidate.fitness > best_chromo.fitness:
            best_chromo = best_candidate

        print(f"Generation {gen + 1}: Best Fitness = {best_chromo.fitness}, F: {F}, CR: {CR}")

    print("\n------------------ Results ------------------")
    print(f"Final Result: \n{np.round(best_chromo.genes).astype(int)}\nFitness: {best_chromo.fitness}")
    return best_chromo

