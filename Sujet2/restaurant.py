# Restaurant
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

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné


def effacer_ecran() : print(CLEARSCR,end = '')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def erase_line() : print("\033[K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
 
NB_SERVEUR = 5
WORKTIME = 1

#----------------------------------------------------------------
def serveur(TableauCommande : list, mutexCommande : Lock, serveurPipe):
    while True :
        mutexCommande.acquire()
        if TableauCommande.__len__() > 0:
            #Prise en charge de la commande
            commande = TableauCommande.pop()
            mutexCommande.release()

            #Transfert à la cuisine
            print("La commande " + commande + " est en cuisine.")
            serveurPipe.send("La commande " + commande + " est en cuisine.")
            time.sleep(5)

            #Le majordome
            serveurPipe.send("La commande " + commande + " est prête.")
            print("La commande " + commande + " est prête.")
        else:
            mutexCommande.release()

def clients(TableauCommande : list, mutexCommande : Lock):
    while True :
        mutexCommande.acquire()
        TableauCommande.append("({},{})".format(random.randint(3,10), 65 + random.randint(0,25)))
        mutexCommande.release()
        print("Une commande a été ajouté au tableau")
        time.sleep(random.randint(3,10))

def majordome(majordomePipe):
    while True :
        text = majordomePipe.recv()
        print(text)

def ouverture_restaurant(ProcessList : list, TableauCommande : list, mutexCommande):
    majordomePipe, serveurPipe = Pipe()

    #Arrivée des employés
    #Majordome
    process = mp.Process(target = majordome, args = (majordomePipe,))
    process.start()
    ProcessList.append(process)

    #Esclaves
    for i in range(NB_SERVEUR):
        process = mp.Process(target = serveur, args = (TableauCommande, mutexCommande, serveurPipe))
        process.start()
        ProcessList.append(process)

    print("Ouverture")

    #Arrivée des clients
    process = mp.Process(target = clients, args = (TableauCommande, mutexCommande))
    process.start()
    ProcessList.append(process)

def fermeture_restaurant(ProcessList : list, TableauCommande : list, mutexCommande):
    #Fin des commandes
    ProcessList[ProcessList.__len__() - 1].terminate()
    print("Arrêt des commandes")
    #Arrêt du service
    mutexCommande.acquire()
    while not TableauCommande.__len__() == 0:
        mutexCommande.release()
        mutexCommande.acquire()
        continue
    mutexCommande.release()
    for i in range(1, NB_SERVEUR + 1):
        ProcessList[i].terminate()
    #Départ du majordome
    ProcessList[0].terminate()
    print("Fermeture")

# ---------------------------------------------------
# La partie principale :
if __name__ == "__main__" :
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujet

    ProcessList = []
    TableauCommande = []
    mutexCommande = Lock()
    ouverture_restaurant(ProcessList, TableauCommande, mutexCommande)
    for i in range(WORKTIME):
        time.sleep(10)
    fermeture_restaurant(ProcessList, TableauCommande, mutexCommande)
