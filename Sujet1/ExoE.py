#FINI (3 points)
import random, time
import multiprocessing as mp 

# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
def frequence_de_hits_pour_n_essais(nb_iteration, pour_fils_to_send):
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
        # si le point est dans l’unit circle
        if x * x + y * y <= 1: count += 1
    pour_fils_to_send.send(count) 

# Nombre d’essai pour l’estimation
nb_total_iteration = 100000000
k_processus = mp.cpu_count()
pour_pere_to_receive, pour_fils_to_send = mp.Pipe()

sum_ite = 0.0
debut = time.time()

for i in range (0, k_processus):
    mp.Process(target=frequence_de_hits_pour_n_essais,args=(nb_total_iteration//k_processus, pour_fils_to_send)).start()

for i in range (0, k_processus):
    sum_ite = sum_ite + pour_pere_to_receive.recv()

print("Valeur estimée Pi par la méthode Multi−Processus : ", 4 * sum_ite / nb_total_iteration)
print("Temps utilisé : ", time.time()-debut)

#TRACE :
# Valeur estimée Pi par la méthode Mono−Processus :  3.14194908
# Temps utilisé :  17.992561101913452

#TRACE :
# Valeur estimée Pi par la méthode Multi−Processus :  3.14160564
# Temps utilisé :  5.295929431915283