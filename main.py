import random 
import time
import tkinter as tk

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

    # se formeaza o populatie de indivizi folosind cromozomii obtinuti
    for cromozom in cromozomi:
        populatie.append(Individ(list(cromozom)))
    
    return populatie

def selectie_turnir(populatie, dim_turnir, dim_populatie):

    populatie_obtinuta = []

    for i in range(dim_populatie):
        # selectare un numar dat de indivizi pentru turnir
        indivizi_selectati = random.sample(populatie, dim_turnir)

        # castiga individul cu cel mai mic fitness
        individ_castigator = min(indivizi_selectati, key=lambda individ: individ.fitness)

        populatie_obtinuta.append(individ_castigator)

    return populatie_obtinuta

def selectare_parinti(populatie):

    parinti = []
    n = len(populatie)

    for i in range(n//2):
        
        parinte1 = selectie_turnir(populatie, 4, 1)[0]
        parinte2 = selectie_turnir(populatie, 4, 1)[0]

        # verificare ca sa nu fie parintii la fel
        while parinte1 == parinte2:
            parinte2 = selectie_turnir(populatie, 4, 1)[0]  

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

    # gasire elemente care se afla pe mai multe pozitii
    # pe una dintre pozitii se pune un element lipsa
    k=0
    for element, valoare in pozitii.items():

        if(len(valoare) > 1):
            i = random.choice(list(valoare))
            copil[i] = lipsa[k]
            k += 1
            
    return copil    

def exista_duplicate(copil):
    return len(set(copil)) < len(copil)

def crossover(parinte1, parinte2):

    taietura = random.randint(0,len(parinte1)-1)

    copil1 =  parinte1[:taietura] + parinte2[taietura:] 
    copil2 =  parinte2[:taietura] + parinte1[taietura:] 

    if exista_duplicate(copil1):
            copil1 = corecteaza_cromozom(copil1)
    if exista_duplicate(copil2):
            copil2 = corecteaza_cromozom(copil2)

    return (copil1, copil2)

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

    # interschimbare elemente de pe pozitiile generate
    cromozom[poz1], cromozom[poz2] = cromozom[poz2], cromozom[poz1]

    # adaugare cromozom schimbat la individ
    individ.cromozom = cromozom

def mutatie(populatie, rata_mutatie):

    for individ in populatie:
        if random.random() < rata_mutatie:
            mutatie_cromozom(individ)
            # recalculare fitness
            individ.calc_fitness()

def verifica_solutii(populatie):
    # verifica daca in populatie exista solutii si le returneaza daca au fost
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

class ChessBoard:
    def __init__(self, master, arrangements, generatie):
        self.master = master
        self.arrangements = arrangements
        self.current_index = 0
        self.generatie = generatie
        
        self.total_label = tk.Label(master, text=f"Solutii gasite in generatia {self.generatie}: {len(arrangements)}", font=("Arial", 14))
        self.total_label.pack()
        self.current_label = tk.Label(master, text=f"Solutia curenta: {arrangements[0].cromozom}", font=("Arial", 14))
        self.current_label.pack()
        
        self.canvas_size = 500  
        self.canvas = tk.Canvas(master, width=self.canvas_size, height=self.canvas_size) 
        self.canvas.pack()
        
        self.next_button = tk.Button(master, text="Next", command=self.show_next)
        self.next_button.pack()
        
        self.queen_image = tk.PhotoImage(file="regina.png")
        
        self.draw_chess_board(arrangements[self.current_index].cromozom)

    def draw_chess_board(self, queens):
        self.canvas.delete("all")
        
        num_queens = len(queens)
        square_size = self.canvas_size // (num_queens + 1)  
        offset = square_size // 2  

        # desenare numere pentru randuri
        for row in range(num_queens):
            self.canvas.create_text(
                offset // 2, row * square_size + square_size // 2 + offset,
                text=str(row), font=("Arial", 14), fill="black"
            )
        
        # desenare numere pentru coloane
        for col in range(num_queens):
            self.canvas.create_text(
                col * square_size + square_size // 2 + offset, offset // 2,
                text=str(col), font=("Arial", 14), fill="black"
            )
        
        # desenare tabel
        for row in range(num_queens):
            for col in range(num_queens):
                color = "white" if (row + col) % 2 == 0 else "black"
                self.canvas.create_rectangle(
                    col * square_size + offset, row * square_size + offset,
                    col * square_size + square_size + offset, row * square_size + square_size + offset,
                    fill=color
                )
        
        # desenare regine
        for col, row in enumerate(queens):
            if row != -1:
                x_center = col * square_size + square_size // 2 + offset
                y_center = row * square_size + square_size // 2 + offset
                self.canvas.create_image(x_center, y_center, image=self.queen_image)

    def show_next(self):
        self.current_index = (self.current_index + 1) % len(self.arrangements)
        current_arrangement = self.arrangements[self.current_index].cromozom
        self.draw_chess_board(current_arrangement)
        self.current_label.config(text=f"Solutia curenta: {current_arrangement}")


def start():
    nr_indivizi = 1000
    n = 12
    max_indivizi = factorial(n)
    rata_mutatie = 0.5
    dim_turnir = 4 # nr de indivizi pt selectia turnir
    dim_populatie = nr_indivizi//2 # nr de indivizi returnati dupa selectia turnir
    generatie_maxima = 200 # numarul generatiei la care se opreste algoritmul 

    # nr_indivizi <= n!, deoarece pot fi generati doar n! indivizi distincti
    if( nr_indivizi > max_indivizi ):
        print(f"Nu se pot genera {nr_indivizi} de indivizi.\
            \nPentru o tabela de {n}x{n} se pot genera maxim {max_indivizi} de indivizi")
        exit(1)

    timp_start = time.time()

    populatie_initiala = generare_populatie_initiala(nr_indivizi, n)
    populatie = selectie_turnir(populatie_initiala, dim_turnir, dim_populatie)
    generatie = 1 
    cel_mai_bun_individ = None

    while not verifica_solutii(populatie) and generatie < generatie_maxima:
        parinti = selectare_parinti(populatie)
        copii = generare_copii(parinti)
        mutatie(copii, rata_mutatie)

        # actualizare cel mai bun individ
        for individ in copii:
            if cel_mai_bun_individ is None or individ.fitness < cel_mai_bun_individ.fitness:
                cel_mai_bun_individ = individ

        generatie += 1
        populatie = copii
    
    timp_executie = time.time() - timp_start

    solutii = verifica_solutii(populatie)
    
    if len(solutii)>0:
        print(f'Solutii gasite in generatia {generatie}: {len(solutii)}')
        for i in solutii:
            print(i.cromozom, i.fitness)
    else:
        print(f'Nu s-au gasit solutii dupa {generatie_maxima} de generatii.')
        if cel_mai_bun_individ:
            print(f'Cea mai buna solutie gasita: {cel_mai_bun_individ.cromozom}, fitness: {cel_mai_bun_individ.fitness}')
            solutii.append(cel_mai_bun_individ) #adaugare in solutii pentru a putea fi afisat in interfata

    print(f'Timp de executie: {timp_executie:.2f} secunde')

    root = tk.Tk()
    root.title("Chess Board")
    chess_board = ChessBoard(root, solutii, generatie)
    root.mainloop()
        
start()