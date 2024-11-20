import random 

class Individ:

    # pozitiile listei cromozom sunt coloanele tablei
    # valorile sunt liniile pe care sunt asezate reginele
    # ex. [1,2,0,3] - pe coloana 0, linia 1 este o regina, pe coloana 1 linia 2 alta regina etc. 
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

    # gasire elemente care se afla pe mai multe pozitii
    # pe una dintre pozitii se pune un element lipsa
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

#crossover([0,1,2,3], [3,1,2,0])
def generare_copii(parinti):

    copii = []

    for (p1, p2) in parinti:
        # crossover returneaza un tuplu cu 2 copii si in lista copii nu dorim tupluri de 2 copii
        copii_obtinuti = crossover(p1.cromozom, p2.cromozom)
        copii.append(Individ(copii_obtinuti[0]))
        copii.append(Individ(copii_obtinuti[1]))

    return copii

def mutatie_cromozom(individ):

    cromozom = individ.cromozom

    # folosire sample pt ca sa nu avem ambele pozitii la fel
    poz1, poz2 = random.sample(range(len(cromozom)), 2)
    # print("pozitii", pozitii)

    # interschimbare elemente de pe pozitiile generate
    cromozom[poz1], cromozom[poz2] = cromozom[poz2], cromozom[poz1]
    # print(cromozom)

    # adaugare cromozom schimbat la individ
    individ.cromozom = cromozom

def mutatie(populatie, rata_mutatie):

    mutatii=0
    for individ in populatie:
        if random.random() < rata_mutatie:
            mutatie_cromozom(individ)
            # recalculare fitness
            individ.calc_fitness()
            mutatii += 1

    # print("Mutatii efectuate:", mutatii)

#mutatie( [Individ([0,2,1,3]), Individ([2,1,3,0])] )

def verifica_solutii(populatie):
    # verifica daca in populatie exista solutii
    solutii = []

    for individ in populatie:
        if individ.fitness == 0:
            solutii.append(individ)
    
    return solutii

def exista_duplicate_copii(copii):
    # verifica daca cel putin un copil are un element duplicat in cromozom
    for copil in copii:
        if exista_duplicate(copil.cromozom):
            return True
    return False

def factorial(n):

    if(n == 1):
        return 1
    
    return n * factorial(n-1) 

def start():
    nr_indivizi = 1000
    n = 10         
    max_indivizi = factorial(n)
    rata_mutatie = 0.5
    
    # nr_indivizi <= n!, deoarece pot fi generati doar n! indivizi distincti
    if( nr_indivizi > max_indivizi ):
        print(f"Nu se pot genera {nr_indivizi} de indivizi.\
            \nPentru o tabela de {n}x{n} se pot genera maxim {max_indivizi} de indivizi")
        exit(1)

    populatie = generare_populatie_initiala(nr_indivizi, n)
    generatie = 1

    while not verifica_solutii(populatie):
        parinti = selectare_parinti(populatie)
        copii = generare_copii(parinti)
        mutatie(copii, rata_mutatie)
        generatie += 1
        populatie = copii
    
    solutii = verifica_solutii(populatie)
    print(f'Solutii gasite in generatia {generatie}: {len(solutii)}')
    for i in solutii:
        print(i.cromozom, i.fitness)
        
start()


# populatie = generare_populatie_initiala(nr_indivizi, n)
#for individ in populatie:
    #print(individ.cromozom, individ.fitness)

# parinti = selectare_parinti(populatie)

#for (p1, p2) in parinti:
    #print(p1.cromozom, p2.cromozom)

#print("Parinti generati: ", len(parinti))
# copii = generare_copii(parinti)
# mutatie(copii, rata_mutatie)

# for copil in copii:
#     print(copil.cromozom, copil.fitness)

# solutii = verifica_solutii(copii)
# print("Solutii copii: ", len(solutii))
# for i in solutii:
#     print(i.cromozom)

# print("Copii obtinuti: ", len(copii))
# print("Exista copii cu elemente duplicate: ", exista_duplicate_copii(copii))
# print("Indivizi in populatie:", len(populatie))
