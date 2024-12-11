import numpy as np
from scipy.optimize import linprog
import tkinter as tk
from tkinter import messagebox

def resolver_programa():
    try:
        # Leer datos ingresados
        funcion_objetivo = list(map(float, entry_objetivo.get().split(',')))
        restricciones = entry_restricciones.get().split(';')
        lados_derechos = list(map(float, entry_lados.get().split(',')))

        # Procesar restricciones
        A = [list(map(float, r.split(','))) for r in restricciones]

        # Resolver el problema
        resultado = linprog(c=funcion_objetivo, A_ub=A, b_ub=lados_derechos, method='highs')

        # Mostrar resultados
        if resultado.success:
            solucion = f"Solución óptima:\n"
            for i, valor in enumerate(resultado.x, start=1):
                solucion += f"x{i} = {valor:.2f}\n"
            solucion += f"Valor óptimo de la función objetivo: {-resultado.fun:.2f}"
        else:
            solucion = "No se pudo encontrar una solución óptima."

        messagebox.showinfo("Resultados", solucion)

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema con los datos: {e}")

# Crear ventana
ventana = tk.Tk()
ventana.title("Programación Lineal")

# Etiquetas y campos de entrada
tk.Label(ventana, text="Función Objetivo (ej: -40,-50):").grid(row=0, column=0, sticky="e")
entry_objetivo = tk.Entry(ventana, width=30)
entry_objetivo.grid(row=0, column=1)

tk.Label(ventana, text="Restricciones (ej: 2,3;4,2):").grid(row=1, column=0, sticky="e")
entry_restricciones = tk.Entry(ventana, width=30)
entry_restricciones.grid(row=1, column=1)

tk.Label(ventana, text="Lados Derechos (ej: 120,160):").grid(row=2, column=0, sticky="e")
entry_lados = tk.Entry(ventana, width=30)
entry_lados.grid(row=2, column=1)

# Botón para resolver
tk.Button(ventana, text="Resolver", command=resolver_programa).grid(row=3, column=1, pady=10)

# Iniciar ventana
ventana.mainloop()
