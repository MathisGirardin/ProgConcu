
# Quelques codes d'échappement (tous ne sont pas utilisés)
import multiprocessing as mp
from time import sleep
import numpy as np


CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

DELAFCURSOR = "\x1B[K"             #  effacer après la position du curseur
CRLF  = "\r\n"                     #  Retour à la ligne

def effacer_ecran() : print(CLEARSCR,end = '')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def erase_line() : print("\033[K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def countNeighbourLive(line, col, tab, i, j):
    count = 0
    if (i != 0) and (tab[i-1,j] == 1): 
        count += 1
    if (i != 0) and j != 0 and (tab[i-1,j-1] == 1): 
        count += 1
    if (j != 0) and (tab[i,j-1] == 1): 
        count += 1
    if (i != line-1) and (j != 0) and (tab[i+1,j-1] == 1): 
        count += 1
    if (i != line-1) and (tab[i+1,j] == 1): 
        count += 1
    if (i != line-1) and (j != col-1) and (tab[i+1,j+1] == 1): 
        count += 1
    if (j != col-1) and (tab[i,j+1] == 1): 
        count += 1
    if (i != 0) and (j != col-1) and (tab[i-1,j+1] == 1): 
        count += 1
    
    return count      

def calcLine(line, col, tab, i):
    tempTab = [0]*col
    for j in range(0, col): 
        voisinsVivants = countNeighbourLive(line, col, tab, i, j) 
        if tab[i][j] == 0:
            if voisinsVivants == 3:
                tempTab[j] = 1
        else:
            if voisinsVivants == 2 or voisinsVivants == 3:
                tempTab[j] = 1
    return tempTab
    
def getNextTab(line, col, tab):
    newTab = np.zeros((line, col))
    listProcess = [0]*line
    for i in range (0, line):
        listProcess[i] = mp.Process(target=calcLine, args=(line, col,tab, i,))
        listProcess[i].start()
        newTab[i] = calcLine(line, col, tab, i)
    return newTab
                    

def showActualTab(line, col, tab):
    effacer_ecran()
    str = "+"
    for i in range(0, col):
        str += "-"
    str += "+"
    print(str)
    for i in range(0, line):
        str="|"
        for j in range (0, col):
            if(tab[i][j]== 0):
                str = str + "■"
            else: str = str +"□"
        str += "|"
        print(str)
    str = "+"
    for i in range(0, col):
        str += "-"
    str += "+"
    print(str)

def gol(line, col, tab):
    while 1:
        showActualTab(line, col, tab)
        tab = getNextTab(line, col, tab)
        sleep(0.2)


col = 39
line = 9
            
pattern = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                    [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
        
print(pattern)

gol(line, col, pattern)
