import time
import multiprocessing
from core.prime_calculator import procesar_bloque_primos
from core.metrics import obtener_uso_recursos

def ejecucion_multiprocessing(rangos):
    print("\n--- INICIANDO EJECUCIÓN CON MULTIPROCESSING ---")
    inicio_tiempo = time.time()
    procesos = []
    cpu_inicio, ram_inicio = obtener_uso_recursos()
    
    for i, (inicio, fin) in enumerate(rangos):
        p = multiprocessing.Process(target=procesar_bloque_primos, args=(inicio, fin, i))
        procesos.append(p)
        p.start() 
        
    for p in procesos:
        p.join()  
        
    tiempo_total = time.time() - inicio_tiempo
    cpu_fin, ram_fin = obtener_uso_recursos()
    return tiempo_total, max(cpu_inicio, cpu_fin), ram_fin - ram_inicio