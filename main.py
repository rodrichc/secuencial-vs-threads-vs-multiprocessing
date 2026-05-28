import psutil
from execution.sequential import ejecucion_secuencial
from execution.thread import ejecucion_threads
from execution.process import ejecucion_multiprocessing
from core.metrics import obtener_info_procesador 

if __name__ == "__main__":
    # Inicializa el medidor de psutil para limpiar registros viejos del SO
    psutil.cpu_percent(interval=None)
    
    nombre_cpu, c_fisicos, h_logicos = obtener_info_procesador()
    
    print("\n=======================================================")
    print("        ENTORNO DE HARDWARE DETECTADO POR EL SO        ")
    print("=======================================================")
    print(f"PROCESADOR: {nombre_cpu}")
    print(f"RECURSOS:   {c_fisicos} Núcleos Físicos | {h_logicos} Hilos Lógicos")
    print("=======================================================")
    

    RANGOS_PRUEBA = [
        (1, 1_000_000),
        (1_000_000, 2_000_000),
        (2_000_000, 3_000_000),
        (3_000_000, 4_000_000)
    ]
    

    t_sec, cpu_sec, ram_sec = ejecucion_secuencial(RANGOS_PRUEBA)
    t_thr, cpu_thr, ram_thr = ejecucion_threads(RANGOS_PRUEBA)
    t_mp, cpu_mp, ram_mp = ejecucion_multiprocessing(RANGOS_PRUEBA)
    

    ram_sec = max(0.0, ram_sec)
    ram_thr = max(0.0, ram_thr)
    ram_mp = max(0.0, ram_mp)
    
    print("\n=======================================================")
    print("        MÉTRICAS FORMALES RECOLECTADAS  ")
    print("=======================================================")
    print(f"SECUENCIAL:      {t_sec:.2f}s | CPU: {cpu_sec}% | RAM: +{ram_sec:.2f} MB")
    print(f"THREADS:         {t_thr:.2f}s | CPU: {cpu_thr}% | RAM: +{ram_thr:.2f} MB")
    print(f"MULTIPROCESSING: {t_mp:.2f}s | CPU: {cpu_mp}% | RAM: +{ram_mp:.2f} MB")
    print("=======================================================\n")