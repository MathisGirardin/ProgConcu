# Restaurant
# Version de Girardin Mathis et Thomas Alexis
from multiprocessing import Pipe, Queue
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

def effacer_ecran() : print(CLEARSCR,end = '')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def erase_line() : print("\033[K",end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
 
NB_SERVEUR = 5
WORKTIME = 10 #Unité de temps
TIME_TO_COOK = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26] #En seconde

TableauCommande = Queue(maxsize = 50)
traitementCommandeEnCours = Queue()

#----------------------------------------------------------------
def serveur(idServeur, toMajordome):
    toMajordome.send(idServeur + "()A")
    while True :
        #Prise en charge de la commande
        commande = str(TableauCommande.get())
        traitementCommandeEnCours.put(None)
        toMajordome.send("TC") #Update Tableau Commande
        toMajordome.send(idServeur + commande + "R")

        #Transfert à la cuisine
        indTTS = ord(commande[commande.index(',') + 1 : commande.index(')')]) - 65
        time.sleep(TIME_TO_COOK[indTTS])

        #Commande servie
        toMajordome.send(idServeur + commande + "P")

def clients(toMajordome):
    while True :
        TableauCommande.put("({},{})".format(random.randint(1,10), chr(65 + random.randint(0,25))))
        toMajordome.send("TC")
        time.sleep(random.randint(2,5))

def majordome(majordomeRecv):
    while True :
        data = str(majordomeRecv.recv())
        if data == "TC": #Update du TableauCommande
            move_to(NB_SERVEUR + 2, 0)
            erase_line()
            print("Nombre de commandes en attente: " + str(TableauCommande.qsize()))
        else: #Message du serveur
            line = int(data[0 : data.index("(")])
            text = "Le serveur " + str(line) + " "
            if data[data.index(")") + 1] == "R": # Réception de la commande (X,Y)
                text = text + "s'occupe de la commande "
                text = text + data[data.index("(") : data.index(")") + 1]
            elif data[data.index(")") + 1] == "P": # La commande (X,Y) est servi
                text = text + "a servi la commande "
                text = text + data[data.index("(") : data.index(")") + 1]
            elif data[data.index(")") + 1] == "A": # Le serveur attend
                text = text + "attend une commande"
            
            move_to(line, 0)
            erase_line()
            print(text)
            if data[data.index(")") + 1] == "P":
                traitementCommandeEnCours.get()

def ouverture_restaurant(ProcessList : list):
    majordomeRecv, toMajordome = Pipe()

    #Arrivée des employés
    #Majordome
    process = mp.Process(target = majordome, args = (majordomeRecv,))
    process.start()
    ProcessList.append(process)

    #Esclaves (ou serveurs)
    for i in range(NB_SERVEUR):
        process = mp.Process(target = serveur, args = (str(i + 1), toMajordome))
        process.start()
        ProcessList.append(process)

    move_to(NB_SERVEUR + 3, 0)
    erase_line()
    print("Ouvert")

    #Arrivée des clients
    process = mp.Process(target = clients, args = (toMajordome,))
    process.start()
    ProcessList.append(process)

def fermeture_restaurant(ProcessList : list):
    #Fin des commandes
    ProcessList[ProcessList.__len__() - 1].terminate()
    move_to(NB_SERVEUR + 3, 0)
    erase_line()
    print("Arrêt des commandes")

    #Arrêt du service
    while not TableauCommande.empty():
        continue
    time.sleep(0.001)
    while not traitementCommandeEnCours.empty():
        continue

    #Départ du majordome et des serveurs
    for i in range(0, NB_SERVEUR + 1):
        ProcessList[i].terminate()

    move_to(NB_SERVEUR + 3, 0)
    erase_line()
    print("Fermer")

# ---------------------------------------------------
# La partie principale :
if __name__ == "__main__" :
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujet

    while True : #Répétition quotidienne de l'ouverture du restaurant
        ProcessList = []
        ouverture_restaurant(ProcessList)
        for i in range(WORKTIME):
            time.sleep(5)
        fermeture_restaurant(ProcessList)
        for i in range(WORKTIME):
            time.sleep(1)
        TableauCommande = Queue(maxsize = 50)
        traitementCommandeEnCours = Queue()

