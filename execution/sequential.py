import time
from core.prime_calculator import procesar_bloque_primos
from core.metrics import obtener_uso_recursos

def ejecucion_secuencial(rangos):
    print("\n--- INICIANDO EJECUCIÓN SECUENCIAL ---")
    inicio_tiempo = time.time()
    cpu_inicio, ram_inicio = obtener_uso_recursos()
    
    for i, (inicio, fin) in enumerate(rangos):
        procesar_bloque_primos(inicio, fin, i)
        
    tiempo_total = time.time() - inicio_tiempo
    cpu_fin, ram_fin = obtener_uso_recursos()
    return tiempo_total, max(cpu_inicio, cpu_fin), ram_fin - ram_inicio