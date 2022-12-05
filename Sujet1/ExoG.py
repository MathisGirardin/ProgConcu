#PAS FINI (5 points)

import math, random
from array import array
import time

def qsort_serie_sequentiel_avec_listes(liste):
    if len(liste) < 2: return liste
    # Pivot = liste[0]
    gche = [X for X in liste[1:] if X <= liste[0]]
    drte = [X for X in liste[1:] if X > liste[0]]
    # Trier chaque moitié "gauche" et "droite" pour regrouper en plaçant "gche" "Pivot" "drte"
    return qsort_serie_sequentiel_avec_listes(gche) + [liste[0]] + qsort_serie_sequentiel_avec_listes(drte)


def version_de_base(N):
    Tab = array('i', [random.randint(0, 2 * N) for _ in range(N)])
    print("Avant : ", Tab)
    start = time.time()
    Tab = qsort_serie_sequentiel_avec_listes(Tab)
    end = time.time()
    print("Après : ", Tab)
    print("Le temps avec 1 seul Process = %f pour un tableau de %d eles " %((end - start)*1000, N))
    
    print("Vérifions que le tri est correct --> ", end='')
    try :
        assert(all([(Tab[i] <= Tab[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n’a pas marché !")
    
version_de_base(50)