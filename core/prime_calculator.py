import os

def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False  
    return True  

def procesar_bloque_primos(inicio, fin, id_tarea):
    print(f"[PID {os.getpid()}] Tarea {id_tarea} iniciada. Buscando primos...")
    contador = 0
    for num in range(inicio, fin):
        if es_primo(num):
            contador += 1
    print(f"[PID {os.getpid()}] Tarea {id_tarea} finalizada. Primos hallados: {contador}")
    return contador