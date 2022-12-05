
# Quelques codes d'échappement (tous ne sont pas utilisés)
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

def showActualTab(line, col, tab):
    effacer_ecran()
    for i in range(0, line):
        str=""
        for j in range (0, col):
            if(tab[i][j]== 0):
                str = str + "■"
            else: str = str +"□"
        print(str)

def gol(line, col, tab):
    showActualTab(line, col, tab)
    

col = 150
line = 5    
tab = [[0]*col]*line

gol(line, col, tab)
