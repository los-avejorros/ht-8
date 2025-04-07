import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# --- Configuración inicial --- #
random.seed(10)  # Para reproducibilidad
NUM_PACIENTES = 100  # Pacientes a simular
TIEMPO_SIMULACION = 480  # 8 horas (en minutos)
INTERVALO_LLEGADA = 5  # Tiempo promedio entre llegadas (minutos)

# --- Parámetros realistas (fuentes citadas en el informe) --- #
# Tiempos de atención (en minutos):
# - Triage: 5-15 min (Fuente: ACEP, 2023)
# - Doctor: 20-40 min (Fuente: BMJ Emergency Medicine)
# - Rayos X: 15-30 min (Fuente: Radiology Society)
TIEMPO_TRIAGE = lambda: random.uniform(5, 15)
TIEMPO_DOCTOR = lambda: random.uniform(20, 40)
TIEMPO_RAYOS_X = lambda: random.uniform(15, 30)

# Probabilidad de necesitar Rayos X: 40% (Fuente: NIH)
PROB_RAYOS_X = 0.4

# Costos por hora (USD):
# - Enfermera: $35/h (Fuente: BLS)
# - Doctor: $150/h (Fuente: Medscape)
# - Rayos X: $100/h (equipo + operador, Fuente: AHRQ)
COSTO_ENFERMERA = 35 / 60  # USD por minuto
COSTO_DOCTOR = 150 / 60
COSTO_RAYOS_X = 100 / 60

# ----- [CLASES Y FUCIONES] ----- #
class Paciente:
    def __init__(self, id):
        self.id = id
        self.severidad = random.randint(1, 5)  # 1 = más urgente
        self.tiempo_llegada = 0
        self.tiempo_salida = 0
        self.tiempo_espera = 0

def triage(env, enfermeras, paciente):
    paciente.tiempo_llegada = env.now
    with enfermeras.request() as req:
        yield req
        yield env.timeout(TIEMPO_TRIAGE())
        print(f"Paciente {paciente.id} (Severidad {paciente.severidad}) completó triage en {env.now:.1f} min")

def atencion_emergencia(env, paciente, doctores, rayos_x, datos):
    # Etapa 1: --> Doctor
    with doctores.request(priority=paciente.severidad) as req:
        yield req
        inicio_doctor = env.now
        yield env.timeout(TIEMPO_DOCTOR())
        fin_doctor = env.now
        print(f"Paciente {paciente.id} atendido por doctor en {fin_doctor:.1f} min")

    # Etapa 2: --> Rayos X (opcional)
    if random.random() < PROB_RAYOS_X:
        with rayos_x.request(priority=paciente.severidad) as req:
            yield req
            inicio_rayos = env.now
            yield env.timeout(TIEMPO_RAYOS_X())
            fin_rayos = env.now
            print(f"Paciente {paciente.id} completó rayos X en {fin_rayos:.1f} min")

    # ---> Registrar datos
    paciente.tiempo_salida = env.now
    paciente.tiempo_espera = paciente.tiempo_salida - paciente.tiempo_llegada
    datos['pacientes'].append(paciente)
    datos['tiempos_espera'].append(paciente.tiempo_espera)
    datos['severidades'].append(paciente.severidad)

def generador_pacientes(env, enfermeras, doctores, rayos_x, datos):
    for i in range(NUM_PACIENTES):
        paciente = Paciente(i)
        env.process(triage(env, enfermeras, paciente))
        env.process(atencion_emergencia(env, paciente, doctores, rayos_x, datos))
        yield env.timeout(random.expovariate(1.0 / INTERVALO_LLEGADA))

# --- Simulación y análisis --- #
def ejecutar_simulacion(config):
    env = simpy.Environment()
    datos = defaultdict(list)
    enfermeras = simpy.Resource(env, capacity=config['enfermeras'])
    doctores = simpy.PriorityResource(env, capacity=config['doctores'])
    rayos_x = simpy.PriorityResource(env, capacity=config['rayos_x'])
    env.process(generador_pacientes(env, enfermeras, doctores, rayos_x, datos))
    env.run(until=TIEMPO_SIMULACION)
    
    # --> Calcular métricas
    df = pd.DataFrame({
        'Severidad': datos['severidades'],
        'Tiempo_Espera': datos['tiempos_espera']
    })
    tiempo_promedio = df['Tiempo_Espera'].mean()
    costo_total = (
        (config['enfermeras'] * COSTO_ENFERMERA * TIEMPO_SIMULACION) +
        (config['doctores'] * COSTO_DOCTOR * TIEMPO_SIMULACION) +
        (config['rayos_x'] * COSTO_RAYOS_X * TIEMPO_SIMULACION)
    )
    
    return df, tiempo_promedio, costo_total

# --- Configuraciones a comparar --- #
configs = [
    {'enfermeras': 2, 'doctores': 3, 'rayos_x': 1},  # Configuración básica
    {'enfermeras': 3, 'doctores': 4, 'rayos_x': 2},  # Configuración óptima
    {'enfermeras': 4, 'doctores': 5, 'rayos_x': 2}   # Configuración costosa
]

# --- Ejecutar simulaciones y generar gráficas --- #
resultados = []
for config in configs:
    df, tiempo_promedio, costo_total = ejecutar_simulacion(config)
    resultados.append({
        'Configuración': f"{config['enfermeras']}E-{config['doctores']}D-{config['rayos_x']}X",
        'Tiempo_Promedio': tiempo_promedio,
        'Costo_Total': costo_total
    })
    print(f"\nConfiguración {config}: Tiempo promedio = {tiempo_promedio:.1f} min, Costo = ${costo_total:.2f}")

# ----- [Crear gráficas] ----- #
df_resultados = pd.DataFrame(resultados)

# Gráfica Tiempo promedio vs. Configuración
plt.figure(figsize=(10, 5))
plt.bar(df_resultados['Configuración'], df_resultados['Tiempo_Promedio'], color='skyblue')
plt.title('Tiempo Promedio de Espera por Configuración de Recursos')
plt.xlabel('Configuración (E=Enfermeras, D=Doctores, X=Rayos X)')
plt.ylabel('Tiempo promedio (minutos)')
plt.grid(axis='y', linestyle='--')
plt.show()

# Gráfica Costo vs. Tiempo
plt.figure(figsize=(10, 5))
plt.scatter(df_resultados['Tiempo_Promedio'], df_resultados['Costo_Total'], s=200, color='red')
for i, row in df_resultados.iterrows():
    plt.text(row['Tiempo_Promedio'], row['Costo_Total'] + 50, row['Configuración'], ha='center')
plt.title('Relación Costo-Tiempo de Espera')
plt.xlabel('Tiempo promedio (minutos)')
plt.ylabel('Costo total (USD)')
plt.grid(True)
plt.show()