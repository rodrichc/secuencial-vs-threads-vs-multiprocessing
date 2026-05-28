import os
import platform
import psutil

def obtener_info_procesador():
    """
    Detecta automáticamente el nombre comercial del procesador y sus núcleos.
    """

    nombre_cpu = platform.processor() or "Procesador Desconocido"
    print(nombre_cpu)
    sistemas_operativos = platform.system()
    

    if sistemas_operativos == "Windows":
        try:
            import subprocess
            comando = "wmic cpu get name"
            resultado = subprocess.check_output(comando, shell=True).decode().split("\n")
            if len(resultado) > 1:
                nombre_cpu = resultado[1].strip()
        except Exception:
            try:
                import winreg
                clave = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                nombre_cpu, _ = winreg.QueryValueEx(clave, "ProcessorNameString")
            except Exception:
                pass


    elif sistemas_operativos == "Linux":
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                for linea in f:
                    if "model name" in linea:
                        nombre_cpu = linea.split(":")[1].strip()
                        break
        except Exception:
            pass

    nucleos_fisicos = psutil.cpu_count(logical=False) 
    hilos_logicos = psutil.cpu_count(logical=True)   
    
    return nombre_cpu, nucleos_fisicos, hilos_logicos

def obtener_uso_recursos():
    proceso_actual = psutil.Process(os.getpid())
    uso_cpu = psutil.cpu_percent(interval=None) 
    
    memoria_bytes = proceso_actual.memory_info().rss
    for hijo in proceso_actual.children(recursive=True):
        try:
            memoria_bytes += hijo.memory_info().rss
        except psutil.NoSuchProcess:
            pass
            
    return uso_cpu, memoria_bytes / (1024 * 1024)