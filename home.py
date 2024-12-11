import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class SimplexMethod:
    def __init__(self, A, b, c, num_variables):
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.c = np.array(c, dtype=float)
        self.num_variables = num_variables
        self.num_constraints = len(b)
        self.tableau = self._initialize_tableau()

    def _initialize_tableau(self):
        """Crea la tabla inicial del método simplex."""
        tableau = np.zeros((self.num_constraints + 1, self.num_variables + self.num_constraints + 1))
        tableau[:-1, :-1] = np.hstack((self.A, np.eye(self.num_constraints)))
        tableau[:-1, -1] = self.b
        tableau[-1, :self.num_variables] = -self.c
        return tableau

    def _pivot_column(self):
        """Encuentra la columna pivote (más negativa en la última fila)."""
        last_row = self.tableau[-1, :-1]
        pivot_col = np.argmin(last_row)
        if last_row[pivot_col] >= 0:
            return None  # Se ha alcanzado la solución óptima
        return pivot_col

    def _pivot_row(self, pivot_col):
        """Encuentra la fila pivote usando la prueba de relación mínima positiva."""
        ratios = []
        for i in range(self.num_constraints):
            if self.tableau[i, pivot_col] > 0:
                ratios.append(self.tableau[i, -1] / self.tableau[i, pivot_col])
            else:
                ratios.append(np.inf)
        pivot_row = np.argmin(ratios)
        if ratios[pivot_row] == np.inf:
            raise ValueError("El problema es no acotado.")
        return pivot_row

    def _perform_pivot(self, pivot_row, pivot_col):
        """Realiza la operación de pivote en la tabla."""
        self.tableau[pivot_row] /= self.tableau[pivot_row, pivot_col]
        for i in range(len(self.tableau)):
            if i != pivot_row:
                self.tableau[i] -= self.tableau[i, pivot_col] * self.tableau[pivot_row]

    def solve(self):
        """Ejecuta el algoritmo simplex y retorna los pasos y resultados."""
        steps = []
        iteration = 1
        while True:
            steps.append(f"Iteración {iteration}:{np.round(self.tableau, 2)}\n")
            pivot_col = self._pivot_column()
            if pivot_col is None:
                steps.append("Se ha alcanzado la solución óptima.\n")
                break
            pivot_row = self._pivot_row(pivot_col)
            steps.append(f"Columna pivote: {pivot_col}, Fila pivote: {pivot_row}\n")
            self._perform_pivot(pivot_row, pivot_col)
            iteration += 1

        solution = np.zeros(self.num_variables)
        for i in range(self.num_constraints):
            if np.count_nonzero(self.tableau[i, :self.num_variables]) == 1:
                var_index = np.argmax(self.tableau[i, :self.num_variables])
                solution[var_index] = self.tableau[i, -1]

        optimal_value = -self.tableau[-1, -1]
        return steps, np.round(solution, 2), round(optimal_value, 2)

    def plot_graphical_method(self):
        """Dibuja el método gráfico para problemas de dos variables."""
        if self.num_variables != 2:
            raise ValueError("El método gráfico solo es válido para problemas con dos variables.")
        
        # Validar restricciones con datos
        valid_constraints = []
        valid_b = []
        for i in range(self.num_constraints):
            if not np.all(self.A[i] == 0) and self.b[i] != 0:
                valid_constraints.append(self.A[i])
                valid_b.append(self.b[i])

        if not valid_constraints:
            raise ValueError("No hay restricciones válidas para graficar.")

        valid_constraints = np.array(valid_constraints)
        valid_b = np.array(valid_b)

        # Determinar el rango de los ejes
        x_min = 0
        x_max = max(valid_b) + 1
        y_min = 0
        y_max = max(valid_b) + 1

        # Generar valores de x
        x = np.linspace(x_min, x_max, 500)
        plt.figure(figsize=(8, 6))

        # Dibujar las restricciones
        for i in range(len(valid_constraints)):
            if valid_constraints[i, 1] != 0:
                y = (valid_b[i] - valid_constraints[i, 0] * x) / valid_constraints[i, 1]
                plt.plot(x, y, label=f"Restricción {i + 1}")
            else:
                plt.axvline(x=valid_b[i] / valid_constraints[i, 0], label=f"Restricción {i + 1}")

        # Dibujar la función objetivo (línea de nivel para diferentes valores)
        y_obj = (valid_b[0] - valid_constraints[0, 0] * x) / valid_constraints[0, 1]
        for i in range(1, len(valid_constraints)):
            y_obj = np.minimum(y_obj, (valid_b[i] - valid_constraints[i, 0] * x) / valid_constraints[i, 1])
        
        plt.plot(x, y_obj, 'r--', label="Función objetivo")

        # Sombrear la región factible (área donde todas las restricciones se cumplen)
        plt.fill_between(x, 0, y_obj, where=(y_obj >= 0), alpha=0.3, color='green')

        # Configuración del gráfico
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xlabel("x₁")
        plt.ylabel("x₂")
        plt.title("Método Gráfico")
        plt.legend()
        plt.grid(True)

        plt.show()


# Interfaz gráfica
class SimplexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método Simplex")

        tk.Label(root, text="¿Cuántas variables tiene el problema?").grid(row=0, column=0)
        self.variable_count_entry = tk.Entry(root, width=5)
        self.variable_count_entry.grid(row=0, column=1)
        tk.Label(root, text="¿Cuántas restricciones tiene el problema?").grid(row=1, column=0)
        self.restriction_count_entry = tk.Entry(root, width=5)
        self.restriction_count_entry.grid(row=1, column=1)
        tk.Button(root, text="Establecer", command=self.set_variables_restrictions).grid(row=1, column=2)

        self.inputs_frame = tk.Frame(root)
        self.inputs_frame.grid(row=2, column=0, columnspan=3)

        self.result_text = tk.Text(root, width=70, height=20)
        self.result_text.grid(row=3, column=0, columnspan=3)

    def set_variables_restrictions(self):
        try:
            self.num_variables = int(self.variable_count_entry.get())
            self.num_restrictions = int(self.restriction_count_entry.get())
            if self.num_variables <= 0 or self.num_restrictions <= 0:
                raise ValueError("El número de variables y restricciones debe ser mayor a 0.")

            # Limpiar frame anterior
            for widget in self.inputs_frame.winfo_children():
                widget.destroy()

            tk.Label(self.inputs_frame, text="Ingrese los coeficientes de las restricciones (A):").grid(row=0, column=0, columnspan=2)
            self.A_entries = []
            for i in range(self.num_restrictions):
                row_entries = []
                tk.Label(self.inputs_frame, text=f"Restricción {i + 1}:").grid(row=i + 1, column=0)
                for j in range(self.num_variables):  # Ingreso dinámico de variables
                    entry = tk.Entry(self.inputs_frame, width=5)
                    entry.grid(row=i + 1, column=j + 1)
                    row_entries.append(entry)
                self.A_entries.append(row_entries)

            tk.Label(self.inputs_frame, text="Ingrese el lado derecho (b):").grid(row=self.num_restrictions + 1, column=0)
            self.b_entries = []
            for i in range(self.num_restrictions):
                entry = tk.Entry(self.inputs_frame, width=5)
                entry.grid(row=self.num_restrictions + 1, column=i + 1)
                self.b_entries.append(entry)

            tk.Label(self.inputs_frame, text="Ingrese los coeficientes del objetivo (c):").grid(row=self.num_restrictions + 2, column=0)
            self.c_entries = []
            for i in range(self.num_variables):  # Ingreso dinámico de coeficientes objetivo
                entry = tk.Entry(self.inputs_frame, width=5)
                entry.grid(row=self.num_restrictions + 2, column=i + 1)
                self.c_entries.append(entry)

            tk.Button(self.inputs_frame, text="Resolver", command=self.solve_simplex).grid(row=self.num_restrictions + 3, column=0, columnspan=3)
            if self.num_variables == 2:
                tk.Button(self.inputs_frame, text="Método Gráfico", command=self.solve_graphical).grid(row=self.num_restrictions + 4, column=0, columnspan=3)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def solve_simplex(self):
        try:
            A = []
            for row_entries in self.A_entries:
                row = [float(entry.get() or 0) for entry in row_entries]
                A.append(row)

            b = [float(entry.get() or 0) for entry in self.b_entries]
            c = [float(entry.get() or 0) for entry in self.c_entries]

            simplex = SimplexMethod(A, b, c, self.num_variables)
            steps, solution, optimal_value = simplex.solve()

            self.result_text.delete(1.0, tk.END)
            for step in steps:
                self.result_text.insert(tk.END, step + "\n")

            solution_text = "\nSolución óptima:\n"
            for i, val in enumerate(solution):
                solution_text += f"x₋{i + 1}: {val}\n"

            self.result_text.insert(tk.END, solution_text)
            self.result_text.insert(tk.END, f"Valor óptimo: {optimal_value}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def solve_graphical(self):
        try:
            A = []
            for row_entries in self.A_entries:
                row = [float(entry.get() or 0) for entry in row_entries]
                A.append(row)

            b = [float(entry.get() or 0) for entry in self.b_entries]
            c = [float(entry.get() or 0) for entry in self.c_entries]

            simplex = SimplexMethod(A, b, c, self.num_variables)
            simplex.plot_graphical_method()

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimplexApp(root)
    root.mainloop()
