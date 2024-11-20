import random 

class Individ:

    cromozom = []
    fitness = 0

    def __init__(self, cromozom):
        self.cromozom = cromozom
        self.calc_fitness()

    def calc_fitness(self):

       atacuri_diagonala = atacuri_diagonale(self.cromozom)

       self.fitness = atacuri_diagonala

def atacuri_diagonale(cromozom):

    atacuri = 0

    for i in range(len(cromozom)-1):
        for j in range(i+1, len(cromozom)):
            if(i != j):
                diferenta_coloane = abs(i-j)
                diferenta_linii = abs(cromozom[i] - cromozom[j])

                if(diferenta_coloane == diferenta_linii):
                    atacuri += 1

    return atacuri

def generare_cromozomi(nr_indivizi, n):

    cromozomi = set()
    
    while(nr_indivizi):
        
        # valorile cromozomului sunt distincte pentru a avea cate o regina pe fiecare linie
        # sample genereaza o lista de n numere distincte din intervalul(0, n-1)
        cromozom = tuple(random.sample(list(range(n)), n))
    
        # se adauga cromozomul obtinut doar daca nu a fost generat deja
        if cromozom not in cromozomi:
            cromozomi.add(cromozom)
            nr_indivizi -= 1

    return list(cromozomi)

def generare_populatie_initiala(nr_indivizi, n):

    populatie = []

    # se genereaza un set de cromozomi
    cromozomi = generare_cromozomi(nr_indivizi, n)
    # print("cromozomi", cromozomi, type(cromozomi))

    # se formeaza o populatie de indivizi folosind cromozomii obtinuti
    for cromozom in cromozomi:
        populatie.append(Individ(list(cromozom)))
    
    return populatie

def selectare_parinti(populatie):

    parinti = []
    n = len(populatie)

    for i in range(n//2):

        parinte1 = populatie[random.randint(0,len(populatie)-1)]
        # print(parinte1.cromozom)
        populatie.remove(parinte1)                      
        
        parinte2 = populatie[random.randint(0,len(populatie)-1)]
        # print(parinte2.cromozom)
        populatie.remove(parinte2)

        parinti.append((parinte1, parinte2))

    return parinti



populatie = generare_populatie_initiala(10, 4)
#for individ in populatie:
    #print(individ.cromozom, individ.fitness)

parinti = selectare_parinti(populatie)

for (p1, p2) in parinti:
    print(p1.cromozom, p2.cromozom)

print("Parinti generati: ", len(parinti))
print("Indivizi in populatie", len(populatie))
