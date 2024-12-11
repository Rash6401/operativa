from scipy.optimize import linprog

def obtener_funcion_objetivo():
    objetivo = input("Ingrese la función objetivo (separada por comas, ej: -40,-50): ")
    return list(map(float, objetivo.split(',')))

def obtener_restricciones():
    restricciones = input("Ingrese las restricciones (separadas por punto y coma, ej: 2,3;4,2): ")
    return [list(map(float, r.split(','))) for r in restricciones.split(';')]

def obtener_lados_derechos():
    lados = input("Ingrese los lados derechos de las restricciones (separados por comas, ej: 120,160): ")
    return list(map(float, lados.split(',')))

def resolver_programacion_lineal(funcion_objetivo, restricciones, lados_derechos):
    # Resolver el problema de programación lineal usando linprog
    resultado = linprog(c=funcion_objetivo, A_ub=restricciones, b_ub=lados_derechos, method='highs')
    
    return resultado

def imprimir_resultados(resultado):
    if resultado.success:
        print("\nSolución óptima encontrada:")
        print(f"Valor óptimo de la función objetivo: Z = {-resultado.fun:.2f}")
        for i, valor in enumerate(resultado.x, start=1):
            print(f"x{i} = {valor:.2f}")
    else:
        print("\nNo se pudo encontrar una solución óptima.")

def imprimir_proceso(funcion_objetivo, restricciones, lados_derechos):
    print("\nDatos ingresados:")
    print(f"Función objetivo: {funcion_objetivo}")
    print("Restricciones:")
    for i, r in enumerate(restricciones, start=1):
        print(f"Restricción {i}: {r[0]}x1 + {r[1]}x2 <= {lados_derechos[i-1]}")
    print(f"Lados derechos: {lados_derechos}")

def main():
    # Obtener datos de entrada
    funcion_objetivo = obtener_funcion_objetivo()
    restricciones = obtener_restricciones()
    lados_derechos = obtener_lados_derechos()
    
    # Imprimir el proceso
    imprimir_proceso(funcion_objetivo, restricciones, lados_derechos)
    
    # Resolver el problema
    resultado = resolver_programacion_lineal(funcion_objetivo, restricciones, lados_derechos)
    
    # Imprimir resultados
    imprimir_resultados(resultado)

if __name__ == '__main__':
    main()
