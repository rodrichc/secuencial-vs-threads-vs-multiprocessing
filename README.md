### Configuración:
#### 1. Crear el entorno virtual:
```bash
python -m venv env
```

#### 2. Activar el entorno:

En Windows:
```bash
.\env\Scripts\Activate.ps1
```

En Linux / macOS:
```bash
source env/bin/activate
```

#### 3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

### Ejecución:

#### Ejecutar rápida sin recolección de datos:

```bash
python main.py
```
#### Ejecutar, recolectar y promediar 3 vueltas:

```bash
python -m experiments.benchmark
```
