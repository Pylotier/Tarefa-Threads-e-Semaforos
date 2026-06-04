import multiprocessing
import time
import random

semaforoNorte: None
semaforoSul: None
pistaNorte: int = 0
pistaSul: int = 0

def init(sNorte, sSul, pNorte, pSul):
    global semaforoNorte
    global semaforoSul
    global pistaSul
    global pistaNorte

    semaforoNorte = sNorte
    semaforoSul = sSul
    pistaSul = pSul
    pistaNorte = pNorte

def main():
    params: int = [0]*12

    for i in range (12):
        params[i] = i

    semaforoNorte = None
    semaforoSul = None

    pistaSul = multiprocessing.Value('i', 0)
    pistaNorte = multiprocessing.Value('i', 0)

    with multiprocessing.Manager() as manager:
        semaforoNorte = manager.Semaphore(1)
        with multiprocessing.Manager() as manager:
            semaforoSul = manager.Semaphore(1)
            with multiprocessing.Pool(processes=12, initializer=init, initargs=(semaforoNorte, semaforoSul, pistaSul, pistaNorte) )as pool:
                pool.map(op, params)
            
def op(id):
    intRandom = random.randint(1, 2)
    
    if (intRandom == 1):
        with semaforoNorte:
            pistaSul.value = id
            print("Avião", id, "Entrou na pista Sul!")
            print("manobrar")
            time.sleep(random.uniform(0.3,0.7) )
            print("taxiar")
            time.sleep(random.uniform(0.5,1) )
            print("decolagem")
            time.sleep(random.uniform(0.6,0.8) )
            print("afastamento")
            time.sleep(random.uniform(0.3,0.8) )
            print("Avião", id, "decolou da pista!")
    elif (intRandom == 2):
        with semaforoSul:  
            pistaNorte.value = id
            print("Avião", id, "Entrou na pista Norte!")
            print("manobrar")
            time.sleep(random.uniform(1,2) )
            print("taxiar")
            time.sleep(random.uniform(1,2) )
            print("decolagem")
            time.sleep(random.uniform(1,2) )
            print("afastamento")
            time.sleep(random.uniform(1,2) )
            print("Avião", id, "decolou da pista!")
    
if __name__ == '__main__':
    main()
