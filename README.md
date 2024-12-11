# operativa
Este código implementa el **Método Simplex** para resolver problemas de programación lineal, y proporciona una interfaz gráfica utilizando **Tkinter**. También ofrece una opción para visualizar los resultados gráficamente, pero solo para problemas con dos variables.

### Explicación del Código:

1. **Clase `SimplexMethod`**:
   - **Atributos**:
     - `A`: matriz de coeficientes de las restricciones.
     - `b`: vector de valores en el lado derecho de las restricciones.
     - `c`: vector de coeficientes de la función objetivo.
     - `num_variables`: número de variables del problema.
     - `num_constraints`: número de restricciones.
   - **Métodos**:
     - `_initialize_tableau`: crea la tabla inicial para el algoritmo simplex.
     - `_pivot_column`: encuentra la columna pivote.
     - `_pivot_row`: encuentra la fila pivote usando la prueba de relación mínima positiva.
     - `_perform_pivot`: realiza una operación de pivote en la tabla.
     - `solve`: ejecuta el algoritmo simplex y retorna los pasos, la solución óptima y el valor óptimo.
     - `plot_graphical_method`: dibuja el método gráfico para problemas con dos variables.

2. **Clase `SimplexApp`**:
   - Se utiliza **Tkinter** para crear una interfaz gráfica donde el usuario puede ingresar el número de variables, restricciones y los coeficientes para resolver el problema de programación lineal.
   - Permite resolver el problema usando el método simplex y visualizar la solución en la interfaz.

### Librerías Instaladas:
1. **NumPy** (`import numpy as np`): Para manejar matrices y operaciones matemáticas.
2. **Tkinter** (`import tkinter as tk`): Para crear la interfaz gráfica del usuario (GUI).
3. **Matplotlib** (`import matplotlib.pyplot as plt`): Para graficar el problema de programación lineal en el método gráfico, solo para problemas de 2 variables.

Para instalar las librerías que se usan en el código, puedes utilizar el gestor de paquetes **pip**. A continuación te indico cómo instalar cada una de ellas desde la línea de comandos (terminal o consola):

1. **NumPy**:
   NumPy es una librería fundamental para el cálculo numérico en Python. Puedes instalarla con el siguiente comando:

   ```bash
   pip install numpy
   ```

2. **Tkinter**:
   Tkinter es una librería estándar en Python para crear interfaces gráficas. Normalmente, Tkinter viene preinstalado con Python. Si no lo tienes instalado, en sistemas basados en Debian (como Ubuntu) puedes instalarlo con:

   ```bash
   sudo apt-get install python3-tk
   ```

   Para otros sistemas operativos, generalmente Tkinter se instala junto con Python, pero si no es el caso, asegúrate de tener Python instalado correctamente o consulta la documentación de tu sistema.

3. **Matplotlib**:
   Matplotlib es una librería para la creación de gráficos. Para instalarla, usa:

   ```bash
   pip install matplotlib
   ```

### Resumen de los comandos de instalación:

```bash
pip install numpy
pip install matplotlib
# Tkinter generalmente no necesita instalación adicional en la mayoría de los sistemas.
```
