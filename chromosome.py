import numpy as np

class Chromosome:
    def __init__(self, no_genes: int, genes: np.ndarray[int] = None, fitness: float = 0.0, min: int = 0, max: int = 5):
        self.no_genes = no_genes
        self.min = min
        self.max = max
        self.fitness = fitness

        if genes is None:
            self.genes = np.random.randint(low=min, high=max + 1, size=(no_genes, no_genes))
        else:
            self.genes = genes

    def __copy__(self):
        return Chromosome(self.no_genes, self.genes.copy(), self.fitness, self.min, self.max)

    def copy_from(self, other):
        self.no_genes = other.no_genes
        self.genes = other.genes.copy()
        self.min = other.min
        self.max = other.max
        self.fitness = other.fitness

    import numpy as np

class Chromosome:
    def __init__(self, no_genes: int, genes: np.ndarray[int] = None, fitness: float = 0.0, min: int = 0, max: int = 5):
        self.no_genes = no_genes
        self.min = min
        self.max = max
        self.fitness = fitness

        if genes is None:
            self.genes = np.random.randint(low=min, high=max + 1, size=(no_genes, no_genes))
        else:
            self.genes = genes

    def __copy__(self):
        return Chromosome(self.no_genes, self.genes.copy(), self.fitness, self.min, self.max)

    def copy_from(self, other):
        self.no_genes = other.no_genes
        self.genes = other.genes.copy()
        self.min = other.min
        self.max = other.max
        self.fitness = other.fitness

    def compute_fitness(self):
        fitness = 0.0

        directions = [
            (-1, 0),   # Sus
            (0, 1),    # Dreapta
            (1, 0),    # Jos
            (0, -1),   # Stânga
            # (-1, -1),  # Diagonală sus-stânga
            # (-1, 1),   # Diagonală sus-dreapta
            # (1, -1),   # Diagonală jos-stânga
            # (1, 1),    # Diagonală jos-dreapta
            # (-2, 0),   # Deasupra central
            # (-1, -1),  # Diagonala stânga sus
            # (-1, 1),   # Diagonala dreapta sus
            # (0, -2),   # Stânga extremă
            # (0, 2),    # Dreapta extremă
            # (1, -1),   # Diagonala stânga jos
            # (1, 1),    # Diagonala dreapta jos
            # (2, 0)     # Sub central
        ]

        
        # directions_extreme = [
        #     (-2, 0),   # Deasupra central
        #     (-1, -1),  # Diagonala stânga sus
        #     (-1, 1),   # Diagonala dreapta sus
        #     (0, -2),   # Stânga extremă
        #     (0, 2),    # Dreapta extremă
        #     (1, -1),   # Diagonala stânga jos
        #     (1, 1),    # Diagonala dreapta jos
        #     (2, 0)     # Sub central
        # ]





        ############################ ALT NOU #########################

        # for i in range(self.no_genes):
        #     for j in range(self.no_genes):
        #         current = self.genes[i][j]
        #         vec = np.zeros(6) 

        #         for di, dj in directions:
        #             ni, nj = i+di, j+dj

        #             if 0<=ni <self.no_genes and 0<= nj< self.no_genes:
        #                 neighbor = self.genes[ni][nj]
        #                 vec[int(neighbor)]+=1
                        
        #         if current == 0: # apa
        #             fitness+=pow(vec[0], vec[0])
        #             if vec[0]<2:
        #                 fitness-=pow(vec[0],sum(vec))
        #         elif current == 1: # plaja
        #             fitness+=pow(vec[1], vec[1])
        #         elif current == 2: # desert
        #             fitness+=pow(vec[2], vec[2])
        #             if vec[2]<1:
        #                 fitness-=pow(sum(vec),sum(vec)-vec[2])
        #         elif current == 3: # campie
        #             fitness+=pow(vec[3], vec[3])
        #         elif current == 4: # padure
        #             fitness+=pow(vec[4], vec[4])
        #         elif current == 5: # munte
        #             fitness+=pow(vec[5], vec[5])
        #             if vec[4]<3:
        #                 fitness-=pow(sum(vec)*vec[5], sum(vec)-vec[5]+vec[4])
















        ############################# NOU #############################








        # for i in range(self.no_genes):
        #     for j in range(self.no_genes):
        #         current = self.genes[i][j]

        #         if current == 2:
        #             fitness += 100


        #         for dj, di in directions:
        #             ni, nj = i+di, j+dj

        #             if 0<=ni <self.no_genes and 0<= nj< self.no_genes:
        #                 neighbor = self.genes[ni][nj]

        #                 if current == 0 and neighbor == 0:
        #                     fitness += 10
        #                 elif current == 0 and neighbor == 1:
        #                     fitness += 5
        #                 elif current == 0 and neighbor > 1:
        #                     fitness -= 1000

        #                 if current == 1 and neighbor == 0:
        #                     fitness += 10
        #                 elif current == 1 and (neighbor == 2 or neighbor == 3):
        #                     fitness += 2.5
        #                 elif current == 1 and neighbor > 3:
        #                     fitness -= 15
        #                 elif current == 1 and neighbor == 1:
        #                     fitness -= 200

        #                 if current == 2 and neighbor == 0:
        #                     fitness -= 100
        #                 elif current == 2 and neighbor == 1:
        #                     fitness += 10
        #                 elif current == 2 and neighbor == 2:
        #                     fitness +=50
        #                 elif current == 2 and neighbor > 2:
        #                     fitness -= 75

        #                 if current == 3 and neighbor == 3:
        #                     fitness += 62.5
        #                 elif current == 3 and neighbor == 4:
        #                     fitness += 25
        #                 elif current == 3 and neighbor == 1:
        #                     fitness += 12.5
        #                 elif current == 3 and (neighbor == 0 or neighbor == 5):
        #                     fitness -= 100

                        
        #                 if current == 4 and neighbor == 4:
        #                     fitness += 30
        #                 elif current == 4 and (neighbor == 3 or neighbor == 5):
        #                     fitness += 11.5
        #                 elif current == 4 and neighbor < 3:
        #                     fitness -= 100

        #                 for ddi, ddj in directions:
        #                     nni, nnj = i+ddi, j+ddj

        #                     if 0 <= nni < self.no_genes and 0 <= nnj < self.no_genes:
        #                         nneighbor = self.genes[nni][nnj]





























        ################# ORIGINAL #########################33






        for i in range(self.no_genes):
            for j in range(self.no_genes):
                current = self.genes[i][j]

                if current==0:
                    fitness+= 5.7
                elif current==1:
                    fitness+=0.3
                elif current==3:
                    fitness+= 4.3
                elif current==2 or current==4:
                    fitness+=2.5
                elif current==5:
                    fitness+1.3

                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    
                    if 0 <= ni < self.no_genes and 0 <= nj < self.no_genes:
                        neighbor = self.genes[ni][nj]

                        if current == 0 and neighbor == 0:
                            fitness+=6.2
                        elif current == 0 and neighbor == 1:
                            fitness+=4.3
                        elif current == 0 and neighbor > 1:
                            fitness= fitness if fitness<0 else -fitness

                        if current == 1 and neighbor == 1:
                            fitness+=0.3
                        elif current == 1 and neighbor == 0:
                            fitness+=6.2
                        elif current == 1 and neighbor > 1:
                            fitness-=20.5

                        if current == 2 and neighbor == 2:
                            fitness+=2.3
                        elif current == 2 and neighbor == 1:
                            fitness+=0.3
                        elif current == 2 and (neighbor == 0 or neighbor > 3):
                            fitness-=7.3

                        if current == 3 and neighbor == 3:
                            fitness+=3.3
                        elif current == 3 and neighbor == 2:
                            fitness-=2.3
                        elif current == 3 and neighbor !=2:
                            fitness+=6.3
                        elif current == 3 and (neighbor == 1 or neighbor == 4):
                            fitness+=3.3
                        elif current == 3 and neighbor == 5:
                            fitness-=1.2

                        if current == 4 and neighbor == 4:
                            fitness+=2.3
                        elif current == 4 and neighbor == 3:
                            fitness+=3
                        elif current == 4 and neighbor == 5:
                            fitness+=3.5
                        elif current == 4 and neighbor == 2:
                            fitness-=5.4

                        if current == 5 and neighbor == 5:
                            fitness+= 1.3
                        elif current == 5 and neighbor == 4:
                            fitness+= 4.5
                        elif current == 5 and neighbor < 4:
                            fitness-=2.7

                        for ddi, ddj in directions:
                            nni, nnj = i+ddi, j+ddj

                            if 0 <= nni < self.no_genes and 0 <= nnj < self.no_genes:
                                nneighbor = self.genes[nni][nnj]

                                if current == 0 and neighbor == 0 and (neighbor == 0 or neighbor == 1):
                                    fitness += 12.3
                                elif current == 0 and neighbor > 1 and nneighbor < 2:
                                    fitness -= 20.7

                                if current == 1 and neighbor > 1 and nneighbor == 1:
                                    fitness -= 9.7
                                elif current == 1 and neighbor > 1 and nneighbor >0:
                                    fitness -= 9.9
                                elif current == 1 and neighbor == 0 and nneighbor == 0:
                                    fitness += 10.9
                                elif current == 1 and neighbor > 1 and neighbor !=0:
                                    fitness == fitness*fitness * -1

                                if current == 2 and neighbor != 2 and nneighbor == 2:
                                    fitness -= 4.5
                                elif current == 2 and neighbor == 2 and nneighbor == 2:
                                    fitness += 12.4

                                if current == 3 and neighbor == 3 and nneighbor == 3:
                                    fitness +=7.3
                                elif current == 3 and neighbor == 2 and neighbor == 0:
                                    fitness -=5.4

                                if current == 4 and neighbor == 4 and nneighbor == 4:
                                    fitness+=4
                                elif current == 4 and neighbor == 5 and neighbor == 0:
                                    fitness-=7.3

                                if current == 5 and neighbor == 5 and nneighbor == 5:
                                    fitness-=2.5
                                elif current == 5 and neighbor != 5 and nneighbor !=5:
                                    fitness-=4.3
                        

        self.fitness = fitness
        return self.fitness