#FINI - 3 points
# Cours hippique
# Version de Girardin Mathis et Thomas Alexis

from multiprocessing import Pipe
from threading import Lock

import multiprocessing as mp
import os, time, math, random, sys, ctypes   
import platform

# Quelques codes d'échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"             #  effacer après la position du curseur
CRLF  = "\r\n"                     #  Retour à la ligne

# Nov 2021
# Course Hippique (version élèves)
# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné

# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

# Une liste de couleurs à affecter aléatoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
             CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN,  CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

HORSE_SIZE = 4 
LONGEUR_COURSE = 150 # Tout le monde aura la même copie (donc no need to have a 'value')
NB_PROCESS = 10
mutex = Lock()
resultat = [0 for i in range(NB_PROCESS)]


def effacer_ecran() : print(CLEARSCR,end = '')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def erase_line() : print("\033[K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !

def write_cheval(ma_ligne, col):
    move_to(ma_ligne + 1,col)         # pour effacer toute ma ligne
    erase_line_from_beg_to_curs()
    if ma_ligne%HORSE_SIZE == 0:
        print("    __")
    elif ma_ligne%HORSE_SIZE == 1:
        print("___( o)>")
    elif ma_ligne%HORSE_SIZE == 2:
        print("\\ <_. )")
    elif ma_ligne%HORSE_SIZE == 3:
        print(" `---'")

# La tache d'un cheval
def un_cheval(ma_ligne : int, keep_running, sender) : # ma_ligne commence à 0
    col=1
    while col < LONGEUR_COURSE and keep_running.value :
        mutex.acquire(True)
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        write_cheval(ma_ligne * HORSE_SIZE, col)
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        write_cheval(ma_ligne * HORSE_SIZE + 1, col)
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        write_cheval(ma_ligne * HORSE_SIZE + 2, col)
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        write_cheval(ma_ligne * HORSE_SIZE + 3, col)
        mutex.release()
        sender.send(ma_ligne)
        col+=1
        time.sleep(0.01 * random.randint(1,5))

# La tache de l'arbitre
def arbitre(keep_running, recv, guess):
    score = [0 for i in range(NB_PROCESS)]
    gagnant = 0
    perdant = 0
    position = 1
    while keep_running.value:
        indice = recv.recv()
        score[indice] = score[indice] + 1
        if score[indice] == LONGEUR_COURSE - 1:
            resultat[indice] = position
            position = position + 1
            continu = False
        for i in range(NB_PROCESS):
            if score[i] > score[gagnant]:
                gagnant = i
            if score[i] <= score[perdant]:
                perdant = i
            if resultat[i] == 0:
                continu = True
            
        mutex.acquire(True)
        en_rouge()
        move_to(NB_PROCESS * HORSE_SIZE + 2, 1)
        erase_line()
        print("Le premier c'est le canarsson " + (gagnant + 1).__str__())
        move_to(NB_PROCESS * HORSE_SIZE + 3, 1)
        erase_line()
        print("Le dernier c'est le canarsson " + (perdant + 1).__str__())
        if not continu:
            move_to(NB_PROCESS * HORSE_SIZE + 4, 1)
            print("Votre canarsson est arrivé en " + resultat[int(guess) - 1].__str__() + "ème position")
            erase_line()
            if resultat[int(guess) - 1] == NB_PROCESS:
                print("Pfouaaaaahahahaha, le nullos !!! Il a finit dernier, pfffhfhfhf...")
            elif resultat[int(guess) - 1] == 1:
                print("IIIIL AAAA GAAAAGNEEEEEEEEEE !!!!! CEEEEEEE IN-CROI-YABLEEEEEEE !!!!")
            else:
                print("Cé dommage... Tu auras plus de chance si tu mises plus...")
        mutex.release()

#------------------------------------------------
# La partie principale :
def course_hippique(keep_running) :
    mes_process = [0 for i in range(NB_PROCESS)]
    recv, sender = Pipe()

    effacer_ecran()
    print("Héé !! Toi là !!! Viens me dire qui sera l'heureux gagnant de la course du MI-LE-NAIREEEEEE !!!? Cé le canarsson (1 - "+ NB_PROCESS.__str__() +"):")
    guess = input()
    effacer_ecran()
    curseur_invisible()
    
    for i in range(NB_PROCESS):  # Lancer     Nb_process  processus
        mes_process[i] = mp.Process(target = un_cheval, args = (i,keep_running,sender))
        mes_process[i].start()

    move_to(NB_PROCESS * HORSE_SIZE + 6, 1)
    en_rouge()
    print("Hééééééé cé patiiiiiii !!!")

    monarbitre = mp.Process(target = arbitre, args = (keep_running,recv,guess))
    monarbitre.start()
    
    for i in range(NB_PROCESS): mes_process[i].join()

    monarbitre.terminate()
    curseur_visible()
    
# ---------------------------------------------------
# La partie principale :
if __name__ == "__main__" :
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
    keep_running=mp.Value(ctypes.c_bool, True)

    course_hippique(keep_running)
