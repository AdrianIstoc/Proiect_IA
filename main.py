from chromosome import Chromosome
from differential import Crossover, Mutation, Selection

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
    generations = 50
    population = [create_chromosome() for _ in range(population_size)]
    F = 0.7
    CR = 0.8

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