import random 

class Individ:

    cromozom = []
    fitness = 0

    def __init__(self, cromozom):
        self.cromozom = cromozom
        self.calc_fitness()

    def calc_fitness(self):

       atacuri_rand=atac_randuri(self.cromozom)
       atacuri_diagonala = atacuri_diagonale(self.cromozom)

       self.fitness = atacuri_rand + atacuri_diagonala
    
def numara_atacuri_rand(regine):

    nr_atacuri = 0
    for i in range(regine):
       nr_atacuri += i

    return nr_atacuri

def atac_randuri(cromozom):

    atacuri = 0
    aparitii = {}

    # numara cate regine sunt pe fiecare rand
    for i in range(len(cromozom)):
        aparitii[cromozom[i]] = cromozom.count(cromozom[i])
    
    # numara atacurile de pe fiecare rand
    for regine in aparitii.values():
        atac_rand = numara_atacuri_rand(regine)
        atacuri += atac_rand
    
    return atacuri

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

populatie = generare_populatie_initiala(10, 4)
for individ in populatie:
    print(individ.cromozom, individ.fitness)
