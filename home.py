import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Datos de ventas
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
ventas = [120, 130, 125, 140, 135, 145, 150, 160, 155, 165, 170, 175]

# Crear un DataFrame
data = pd.DataFrame({'Mes': meses, 'Ventas': ventas})

# 1. Promedios móviles
def promedio_movil(datos, n):
    return datos.rolling(window=n).mean()

data['Promedio Movil (3 meses)'] = promedio_movil(data['Ventas'], 3)

# 2. Suavización Exponencial
def suavizacion_exponencial(datos, alpha):
    return datos.ewm(alpha=alpha, adjust=False).mean()

data['Suavización Exponencial (α=0.3)'] = suavizacion_exponencial(data['Ventas'], 0.3)

# Mostrar resultados
print(data)

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(data['Mes'], data['Ventas'], label='Ventas reales', marker='o')
plt.plot(data['Mes'], data['Promedio Movil (3 meses)'], label='Promedio móvil (3 meses)', linestyle='--')
plt.plot(data['Mes'], data['Suavización Exponencial (α=0.3)'], label='Suavización exponencial (α=0.3)', linestyle='--')
plt.xticks(rotation=45)
plt.legend()
plt.title('Métodos de Pronóstico')
plt.xlabel('Mes')
plt.ylabel('Ventas')
plt.grid()
plt.show()

