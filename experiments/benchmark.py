import csv
import os
import psutil
from execution.sequential import ejecucion_secuencial
from execution.thread import ejecucion_threads
from execution.process import ejecucion_multiprocessing
from core.metrics import obtener_info_procesador

def correr_bucle_benchmark(vueltas=3):
    print(f"\n=======================================================")
    # Inicializa el medidor global de psutil antes de arrancar el laboratorio
    psutil.cpu_percent(interval=None)
    
    # Cargamos el mismo rango pesado de números primos para estresar la máquina
    RANGOS_PRUEBA = [
        (1, 1_000_000),
        (1_000_000, 2_000_000),
        (2_000_000, 3_000_000),
        (3_000_000, 4_000_000)
    ]
    
    # Diccionario para acumular las métricas de cada vuelta
    historial = {
        "Secuencial": {"tiempo": 0, "cpu": 0, "ram": 0},
        "Threads": {"tiempo": 0, "cpu": 0, "ram": 0},
        "Multiprocessing": {"tiempo": 0, "cpu": 0, "ram": 0}
    }
    
    # Ejecución de los experimentos repetidos
    for v in range(1, vueltas + 1):
        print(f"\n>>> INICIANDO VUELTA {v} DE {vueltas} <<<")
        
        # 1. Test Secuencial
        t_sec, cpu_sec, ram_sec = ejecucion_secuencial(RANGOS_PRUEBA)
        historial["Secuencial"]["tiempo"] += t_sec
        historial["Secuencial"]["cpu"] += cpu_sec
        historial["Secuencial"]["ram"] += ram_sec
        
        # 2. Test Threads
        t_thr, cpu_thr, ram_thr = ejecucion_threads(RANGOS_PRUEBA)
        historial["Threads"]["tiempo"] += t_thr
        historial["Threads"]["cpu"] += cpu_thr
        historial["Threads"]["ram"] += ram_thr
        
        # 3. Test Multiprocessing
        t_mp, cpu_mp, ram_mp = ejecucion_multiprocessing(RANGOS_PRUEBA)
        historial["Multiprocessing"]["tiempo"] += t_mp
        historial["Multiprocessing"]["cpu"] += cpu_mp
        historial["Multiprocessing"]["ram"] += ram_mp

    # Obtenemos los datos del hardware real
    nombre_cpu, c_fisicos, h_logicos = obtener_info_procesador()

    print("\n=======================================================")
    print("        ENTORNO DE HARDWARE DETECTADO POR EL SO        ")
    print("=======================================================")
    print(f"PROCESADOR: {nombre_cpu}")
    print(f"RECURSOS:   {c_fisicos} Núcleos Físicos | {h_logicos} Hilos Lógicos")
    print("=======================================================")

    # Estructura final para calcular y guardar los promedios
    promedios = []
    print("\n=======================================================")
    print("        PROMEDIOS FINALES RECOLECTADOS (BENCHMARK)     ")
    print("=======================================================")
    
    for estrategia, metricas in historial.items():
        p_tiempo = metricas["tiempo"] / vueltas
        p_cpu = metricas["cpu"] / vueltas
        p_ram = metricas["ram"] / vueltas
        
        # Parche de seguridad para que los residuos de limpieza del SO no den negativos en consola
        p_ram = max(0.0, p_ram)
        
        print(f"{estrategia.upper()}: Promedio {p_tiempo:.2f}s | CPU: {p_cpu:.1f}% | RAM: +{p_ram:.2f} MB")
        
        # Guardamos los datos formateados sumando el modelo de procesador detectado
        promedios.append({
            "Procesador": nombre_cpu,
            "Estrategia": estrategia,
            "Tiempo Promedio (s)": round(p_tiempo, 2),
            "CPU Promedio (%)": round(p_cpu, 1),
            "RAM Promedio (MB)": round(p_ram, 2)
        })
        
    # Le pasamos la lista con el procesador incluido a la función de guardado
    guardar_en_csv(promedios)

def guardar_en_csv(datos_promedio):
    # Definimos la ruta asegurando que apunte a la carpeta reports/
    ruta_csv = os.path.join("reports", "results.csv")
    
    # Creamos la carpeta reports si es que no existe todavía
    os.makedirs("reports", exist_ok=True)
    
    # Añadimos la columna "Procesador" al encabezado del CSV
    columnas = ["Procesador", "Estrategia", "Tiempo Promedio (s)", "CPU Promedio (%)", "RAM Promedio (MB)"]
    
    try:
        with open(ruta_csv, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader()  # Escribe los títulos de las columnas
            escritor.writerows(datos_promedio) # Escribe las filas con los promedios e info de CPU
        print(f"\n[OK] Éxito: Métricas y procesador guardados correctamente en '{ruta_csv}'")
    except Exception as e:
        print(f"\n[ERROR] No se pudo guardar el archivo CSV: {e}")

if __name__ == "__main__":
    correr_bucle_benchmark(vueltas=3)