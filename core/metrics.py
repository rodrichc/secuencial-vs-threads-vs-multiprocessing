import os
import platform
import psutil

def obtener_info_procesador():
    """
    Detecta automáticamente el nombre comercial del procesador y sus núcleos.
    """
    nombre_cpu = platform.processor()
    
    # Si estás en Windows, platform.processor() da el nombre técnico de la familia.
    # Con esto lo parchamos para sacar el nombre comercial real:
    if platform.system() == "Windows":
        try:
            # Usamos un comando nativo de Windows para interrogar al hardware
            import subprocess
            comando = "wmic cpu get name"
            resultado = subprocess.check_output(comando, shell=True).decode().split("\n")
            if len(resultado) > 1:
                nombre_cpu = resultado[1].strip()
        except Exception:
            # Si algo falla, intentamos por el registro de Windows
            try:
                import winreg
                clave = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                nombre_cpu, _ = winreg.QueryValueEx(clave, "ProcessorNameString")
            except Exception:
                pass # Si todo falla, se queda con el nombre por defecto de platform
                
    # Contamos los fierros reales
    nucleos_fisicos = psutil.cpu_count(logical=False) # Núcleos reales de silicio
    hilos_logicos = psutil.cpu_count(logical=True)   # Hilos totales (Hyper-Threading)
    
    return nombre_cpu, nucleos_fisicos, hilos_logicos

def obtener_uso_recursos():
    """Tu función de métricas actual"""
    proceso_actual = psutil.Process(os.getpid())
    uso_cpu = psutil.cpu_percent(interval=None) 
    
    memoria_bytes = proceso_actual.memory_info().rss
    for hijo in proceso_actual.children(recursive=True):
        try:
            memoria_bytes += hijo.memory_info().rss
        except psutil.NoSuchProcess:
            pass
            
    return uso_cpu, memoria_bytes / (1024 * 1024)