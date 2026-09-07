# Problema damelor

Rezolvare pentru problema damelor folosind un algoritm genetic în Python. Programul caută aranjamente pentru `n` dame astfel încât nicio pereche de dame să nu se atace pe diagonală.

## Cerințe

- Python 3
- Tkinter, inclus de obicei în instalarea standard Python
- Fișierul `regina.png` în același director cu `main.py`

## Rulare

Din directorul proiectului:

```bash
python main.py
```

Programul afișează în terminal rezultatele și timpul de execuție, apoi deschide o fereastră în care pot fi vizualizate soluțiile găsite. Butonul **Next** trece la următoarea soluție.

## Cum funcționează

Un cromozom este o permutare a numerelor de la `0` la `n - 1`:

```text
[1, 3, 0, 2]
```

Poziția din listă reprezintă coloana, iar valoarea reprezintă linia unei dame. Deoarece valorile sunt distincte, există câte o singură damă pe fiecare linie și coloană.

Algoritmul:

1. Generează populația inițială de cromozomi unici.
2. Evaluează fiecare individ prin numărul de atacuri diagonale.
3. Selectează părinți prin selecție de tip turnir.
4. Creează copii prin crossover și corectează duplicatele apărute.
5. Aplică mutații prin interschimbarea a două poziții.
6. Repetă procesul până găsește o soluție cu fitness `0` sau ajunge la numărul maxim de generații.

## Configurare

Parametrii principali se află în funcția `start()` din `main.py`:

- `nr_indivizi` - dimensiunea populației inițiale;
- `n` - dimensiunea tablei și numărul damelor;
- `rata_mutatie` - probabilitatea aplicării unei mutații;
- `generatie_maxima` - numărul maxim de generații analizate.

Fitness-ul este numărul de perechi de dame care se atacă pe diagonală. Prin urmare, un fitness egal cu `0` reprezintă o soluție validă.

