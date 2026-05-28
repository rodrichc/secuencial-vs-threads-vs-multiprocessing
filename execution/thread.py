import time
import threading
from core.prime_calculator import procesar_bloque_primos
from core.metrics import obtener_uso_recursos

def ejecucion_threads(rangos):
    print("\n--- INICIANDO EJECUCIÓN CON THREADS ---")
    inicio_tiempo = time.time()
    hilos = []
    cpu_inicio, ram_inicio = obtener_uso_recursos()
    
    for i, (inicio, fin) in enumerate(rangos):
        t = threading.Thread(target=procesar_bloque_primos, args=(inicio, fin, i))
        hilos.append(t)
        t.start() 
        
    for t in hilos:
        t.join()  
        
    tiempo_total = time.time() - inicio_tiempo
    cpu_fin, ram_fin = obtener_uso_recursos()
    return tiempo_total, max(cpu_inicio, cpu_fin), ram_fin - ram_inicio