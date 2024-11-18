import random 

class Individ:

    cromozom = []
    fitness = 0

    def __init__(self, cromozom):
        self.cromozom = cromozom
        self.calc_fitness()

    def calc_fitness(self):

       ...

def generare_populatie(nr_indivizi, n):

    cromozomi = set()
    
    while(nr_indivizi):

        cromozom = tuple(random.sample(list(range(n)), k=n))
    
        if cromozom not in cromozomi:
            cromozomi.add(cromozom)
            nr_indivizi -= 1

    return cromozomi

populatie = generare_populatie(10, 4)
for individ in populatie:
    print(individ)
