#FINI - 5 points

from time import sleep
import multiprocessing as mp

def worker(nbill, nbprocess, nbbillesactu, verrou, m, e):
    for i in range (0, m):
        print("Billes demandées : " + str(nbill) + " par " + str(nbprocess))
        ask(nbill, nbbillesactu, verrou, e)
        print("Billes obtenues : " + str(nbill) + " par " + str(nbprocess))
        print("Travail en cours : " + str(nbprocess))
        sleep(3)
        print("Travail fini : " + str(nbprocess))
        ret(nbill, nbbillesactu, verrou, e)

def ask(nbill, nbbillesactu, verrou, e):
    verrou.acquire()
    while nbbillesactu.value < nbill:
        verrou.release()
        e.wait()
        verrou.acquire()
    verrou.release()
    nbbillesactu.value -= nbill


def ret(nbill, nbbillesactu, verrou, e):
    verrou.acquire()
    nbbillesactu.value += nbill
    verrou.release()
    e.set()

def control(maxbill, nbbillesactu, verrou):
    while True:
        verrou.acquire()
        if nbbillesactu.value >= 0 and nbbillesactu.value <= maxbill:
            verrou.release()
        else :
            verrou.release()
            print("Nombre de billes invalides")
        sleep(1)


if __name__ == "__main__":
    m = 5
    nbprocess = 4
    maxbill = 4

    e = mp.Event()

    verrou = mp.Lock()
    variable_partagee = mp.Value('i',maxbill)

    listProcess = [0]*nbprocess
    for i in range(0, nbprocess):
        listProcess[i] = mp.Process(target=worker, args=(i+1, i, variable_partagee,verrou, m, e))
        listProcess[i].start()
    controller = mp.Process(target=control, args=(maxbill, variable_partagee,verrou))
    controller.start()
    for i in range(0, nbprocess):
        listProcess[i].join()
    controller.terminate()