import numpy as np
import tkinter as tk
from tkinter import messagebox

class SimplexMethod:
    def __init__(self, A, b, c):
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.c = np.array(c, dtype=float)
        self.num_variables = len(c)
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
            steps.append(f"Iteración {iteration}:\n{self.tableau}\n")
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
        return steps, solution, optimal_value

# Interfaz gráfica
class SimplexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método Simplex")

        tk.Label(root, text="¿Cuántas restricciones tiene el problema?").grid(row=0, column=0)
        self.restriction_count_entry = tk.Entry(root, width=5)
        self.restriction_count_entry.grid(row=0, column=1)
        tk.Button(root, text="Establecer", command=self.set_restrictions).grid(row=0, column=2)

        self.inputs_frame = tk.Frame(root)
        self.inputs_frame.grid(row=1, column=0, columnspan=3)

        self.result_text = tk.Text(root, width=70, height=20)
        self.result_text.grid(row=3, column=0, columnspan=3)

    def set_restrictions(self):
        try:
            self.num_restrictions = int(self.restriction_count_entry.get())
            if self.num_restrictions <= 0:
                raise ValueError("El número de restricciones debe ser mayor a 0.")

            # Limpiar frame anterior
            for widget in self.inputs_frame.winfo_children():
                widget.destroy()

            tk.Label(self.inputs_frame, text="Ingrese los coeficientes de las restricciones (A):").grid(row=0, column=0, columnspan=2)
            self.A_entries = []
            for i in range(self.num_restrictions):
                row_entries = []
                tk.Label(self.inputs_frame, text=f"Restricción {i + 1}:").grid(row=i + 1, column=0)
                for j in range(5):  # Máximo 5 variables para simplicidad
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
            for i in range(5):  # Máximo 5 variables para simplicidad
                entry = tk.Entry(self.inputs_frame, width=5)
                entry.grid(row=self.num_restrictions + 2, column=i + 1)
                self.c_entries.append(entry)

            tk.Button(self.inputs_frame, text="Resolver", command=self.solve_simplex).grid(row=self.num_restrictions + 3, column=0, columnspan=6)

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

            simplex = SimplexMethod(A, b, c)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = SimplexApp(root)
    root.mainloop()
