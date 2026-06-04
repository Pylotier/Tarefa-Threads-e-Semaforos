import multiprocessing
import time
import random

semaforoTocha: None
semaforoPedra: None
semaforoPortas: None
portas: int = []
pegarTocha: int = 0
pegarPedra: int = 0
cont: int = 0
i:int = 0

def init(sPedra, sPortas, sTocha, porta, pTocha, pPedra, contador):
    global semaforoPedra
    global semaforoPortas
    global semaforoTocha
    global portas
    global pegarTocha
    global pegarPedra
    global cont

    semaforoPedra = sPedra
    semaforoPortas = sPortas
    semaforoTocha = sTocha
    portas = porta
    pegarPedra = pPedra
    pegarTocha = pTocha
    cont = contador

def main():
    params: int = [0]*4

    for i in range (4):
        params[i] = i

    vet_inicial: int = [0]*4
    portas = multiprocessing.Array('i', vet_inicial)
    pegarTocha = multiprocessing.Value('i', 1)
    pegarPedra = multiprocessing.Value('i', 1)
    cont = multiprocessing.Value('i', 0)

    with multiprocessing.Manager() as manager:
        semaforoPedra = manager.Semaphore(1)
        with multiprocessing.Manager() as manager:
            semaforoPortas = manager.Semaphore(1)
            with multiprocessing.Manager() as manager:
                semaforoTocha = manager.Semaphore(1)
                with multiprocessing.Pool(processes=4, initializer=init, initargs=(semaforoPedra, semaforoPortas, semaforoTocha, portas, pegarTocha, pegarPedra, cont)) as pool:
                    pool.map(op, params)
                    
def op(id):
    distanciaPercorrida: int = 0
    portaEscolha: int = 0
    temTocha:int = 0
    temPedra:int = 0
    
    while (distanciaPercorrida <= 2000 and temTocha != 1 and temPedra != 1):
        distanciaPercorrida += random.randint(2,4)
        time.sleep(0.05)
        #print("Cavaleiro",id, "distancia: ", distanciaPercorrida)

        if (pegarTocha.value == 1 and distanciaPercorrida >= 500):
            with semaforoTocha:
                print("Cavaleiro", id, "pegou a tocha")
                pegarTocha.value = 0
                temTocha = 1
                print("Cavaleiro", id, "teve sua velocidade aumentada")

        if (pegarPedra.value == 1 and distanciaPercorrida >= 1500):
            with semaforoPedra:
                print("Cavaleiro", id, "pegou a pedra")
                pegarPedra.value = 0
                temPedra = 1
                print("Cavaleiro", id, "teve sua velocidade aumentada")
           
        if (distanciaPercorrida >= 2000):
            break;

    while(distanciaPercorrida <= 2000):
        distanciaPercorrida += random.randint(2,4) + 2
        time.sleep(0.05)
        
    with semaforoPortas:
        print("Cavaleiro", id, "chegou na escolha das portas")
        portaEscolha = random.randint(1,4)
        print("Cavaleiro", id, "escolhe a porta", portaEscolha)
        i = cont.value
        while portaEscolha in portas:
            # print("porta ocupada")
            portaEscolha = random.randint(1,4)
        portas[i] = portaEscolha
        if (portaEscolha != 3):
            print("Cavaleiro", id, "morreu por um monstro")
        else:
            print("Cavaleiro", id, "escapou e sobreviveu")
        cont.value += 1
        # print(i)
        # print(cont.value)
if __name__ == '__main__':
    main()
