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

def corecteaza_cromozom(copil):

    n = len(copil)
    
    # gasire elemente lipsa
    lipsa = []
    for i in range(n):
        if i not in set(copil):
            lipsa.append(i)  
            
    # gaseste pozitiile tuturor elementelor din copil
    # cheia = elementul, valoarea = set cu pozitiile (ex. 0: {2, 3} )
    pozitii = {}
    for pozitie, element in enumerate(copil):
        if element in pozitii:
            pozitii[element].add(pozitie)
        else:
            pozitii[element] = {pozitie}

    # print("pozitii:", pozitii)        

    # gasire element care se afla pe mai multe pozitii
    # pe una dintre pozitii se pune elementul lipsa
    k=0
    for element, valoare in pozitii.items():

        if(len(valoare) > 1):
            # print(element, valoare)
            i = random.choice(list(valoare))
            copil[i] = lipsa[k]
            k += 1
            
    return copil    

# print(corecteaza_cromozom([0,1,2,0]))

def exista_duplicate(copil):
    return len(set(copil)) < len(copil)
#print(exista_duplicate([1,2,3,1]))

def crossover(parinte1, parinte2):

    #print("\nparinti:", parinte1, parinte2)
    taietura = random.randint(0,len(parinte1)-1)
    #print(taietura)

    copil1 =  parinte1[:taietura] + parinte2[taietura:] 
    copil2 =  parinte2[:taietura] + parinte1[taietura:] 

    if exista_duplicate(copil1):
            # print(copil1)
            copil1 = corecteaza_cromozom(copil1)
    if exista_duplicate(copil2):
            # print(copil2)
            copil2 = corecteaza_cromozom(copil2)

    # print("copii", copil1, copil2)
    return (copil1, copil2)

crossover([0,1,2,3], [3,1,2,0])

populatie = generare_populatie_initiala(10, 4)
#for individ in populatie:
    #print(individ.cromozom, individ.fitness)

parinti = selectare_parinti(populatie)

for (p1, p2) in parinti:
    print(p1.cromozom, p2.cromozom)

print("Parinti generati: ", len(parinti))
print("Indivizi in populatie", len(populatie))
