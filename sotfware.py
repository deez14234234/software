import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


st.title("Mi Software de Análisis")
st.write("Bienvenido al software de análisis en Python.")

tipo = st.selectbox("Tipo de problema", ["Maximización", "Minimización"])
num_restricciones = st.slider("Número de restricciones", 1, 5, 2)
class SolverPL:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema")
        self.root.configure(bg="#f0f4f8")

        # Tamaño fijo centrado
        ancho, alto = 720, 650
        self.root.geometry(f"{ancho}x{alto}")
        self.root.resizable(False, False)
        x_centro = int(self.root.winfo_screenwidth() / 2 - ancho / 2)
        y_centro = int(self.root.winfo_screenheight() / 2 - alto / 2)
        self.root.geometry(f"+{x_centro}+{y_centro}")

        self.tipo_var = tk.StringVar(value="Maximización")
        self.num_restr_var = tk.IntVar(value=2)

        self.crear_widgets()

    def crear_widgets(self):
        titulo = tk.Label(self.root, text="Sistema de programacion lineal", font=("Helvetica", 18, "bold"), bg="#f0f4f8", fg="#333")
        titulo.pack(pady=(20, 10))

        contenedor = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        contenedor.pack(padx=30, pady=10, fill="both", expand=True)

        tipo_frame = tk.Frame(contenedor, bg="#ffffff")
        tipo_frame.pack(pady=5)
        ttk.Label(tipo_frame, text="Tipo de problema:").pack(side="left", padx=5)
        tipo_menu = ttk.Combobox(tipo_frame, textvariable=self.tipo_var, values=["Maximización", "Minimización"], state="readonly", width=15)
        tipo_menu.pack(side="left", padx=5)

        rest_frame = tk.Frame(contenedor, bg="#ffffff")
        rest_frame.pack(pady=5)
        ttk.Label(rest_frame, text="Número de restricciones:").pack(side="left", padx=5)
        tk.Spinbox(rest_frame, from_=1, to=5, textvariable=self.num_restr_var, width=5, command=self.generar_formulario).pack(side="left", padx=5)

        ttk.Separator(contenedor, orient="horizontal").pack(fill="x", pady=10)

        self.obj_frame = tk.LabelFrame(contenedor, text="Función Objetivo", bg="#ffffff", font=("Helvetica", 10, "bold"))
        self.obj_frame.pack(fill="x", padx=10, pady=5)

        self.rest_frame = tk.LabelFrame(contenedor, text="Restricciones", bg="#ffffff", font=("Helvetica", 10, "bold"))
        self.rest_frame.pack(fill="both", expand=True, padx=10, pady=5)

        btn_resolver = tk.Button(contenedor, text="Resolver", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=self.resolver)
        btn_resolver.pack(pady=10)

        self.generar_formulario()

    def generar_formulario(self):
        for widget in self.obj_frame.winfo_children(): widget.destroy()
        for widget in self.rest_frame.winfo_children(): widget.destroy()

        self.sign_vars = []
        self.c_vars = []
        for i in range(2):
            frame = tk.Frame(self.obj_frame, bg="#ffffff")
            frame.pack(pady=2)
            sign = ttk.Combobox(frame, values=["+", "-"], width=3, state="readonly")
            sign.set("+")
            sign.pack(side="left", padx=2)
            coef = ttk.Entry(frame, width=8)
            coef.pack(side="left", padx=2)
            tk.Label(frame, text=f"x{i+1}", bg="#ffffff").pack(side="left")
            self.sign_vars.append(sign)
            self.c_vars.append(coef)

        self.a_vars, self.signos, self.b_vars = [], [], []
        for i in range(self.num_restr_var.get()):
            fila = tk.Frame(self.rest_frame, bg="#ffffff")
            fila.pack(pady=2)
            fila_vars = []
            for j in range(2):
                e = ttk.Entry(fila, width=6)
                e.pack(side="left", padx=3)
                tk.Label(fila, text=f"x{j+1}", bg="#ffffff").pack(side="left", padx=1)
                fila_vars.append(e)
            self.a_vars.append(fila_vars)
            signo = ttk.Combobox(fila, values=["<=", ">=", "="], width=4, state="readonly")
            signo.set("<=")
            signo.pack(side="left", padx=3)
            self.signos.append(signo)
            b = ttk.Entry(fila, width=6)
            b.pack(side="left", padx=3)
            self.b_vars.append(b)

    def resolver(self):
        try:
            tipo = self.tipo_var.get()
            c = [(-1 if self.sign_vars[i].get() == '-' else 1) * float(self.c_vars[i].get()) for i in range(2)]

            A, b, signos = [], [], []
            for i in range(self.num_restr_var.get()):
                fila = [float(self.a_vars[i][j].get()) for j in range(2)]
                A.append(fila)
                b.append(float(self.b_vars[i].get()))
                signos.append(self.signos[i].get())

            norm_rest = []
            for i in range(len(A)):
                a1, a2 = A[i]
                bi = b[i]
                if signos[i] == '<=':
                    norm_rest.append([a1, a2, bi])
                elif signos[i] == '>=':
                    norm_rest.append([-a1, -a2, -bi])
                elif signos[i] == '=':
                    norm_rest.append([a1, a2, bi])

            def intersec(r1, r2):
                a1, a2, b1 = r1
                c1, c2, b2 = r2
                det = a1*c2 - c1*a2
                if det == 0: return None
                x = (b1*c2 - b2*a2) / det
                y = (a1*b2 - c1*b1) / det
                return [x, y]

            puntos = [[0, 0]]
            for a1, a2, b_ in norm_rest:
                if a2 != 0: puntos.append([0, b_/a2])
                if a1 != 0: puntos.append([b_/a1, 0])
            for i in range(len(norm_rest)):
                for j in range(i+1, len(norm_rest)):
                    p = intersec(norm_rest[i], norm_rest[j])
                    if p: puntos.append(p)

            factibles = []
            for x, y in puntos:
                if x < 0 or y < 0: continue
                if all(a1*x + a2*y <= b_ + 1e-6 for a1, a2, b_ in norm_rest):
                    factibles.append([x, y])
            if not factibles:
                messagebox.showerror("Sin solución", "No hay solución factible.")
                return

            soluciones = [{"punto": p, "z": c[0]*p[0] + c[1]*p[1]} for p in factibles]
            optimo = max(soluciones, key=lambda d: d["z"]) if tipo == "Maximización" else min(soluciones, key=lambda d: d["z"])
            messagebox.showinfo("Resultado", f"Z = {optimo['z']:.2f}\nx₁ = {optimo['punto'][0]:.2f}\nx₂ = {optimo['punto'][1]:.2f}")
            self.graficar(norm_rest, factibles, optimo["punto"])
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def graficar(self, restricciones, factibles, optimo):
        fig, ax = plt.subplots()
        x_vals = np.linspace(0, 20, 400)
        for a1, a2, b in restricciones:
            if a2 != 0:
                y_vals = (b - a1 * x_vals) / a2
                ax.plot(x_vals, y_vals, label=f'{a1:.0f}x₁ + {a2:.0f}x₂ ≤ {b:.0f}')
            elif a1 != 0:
                x = b / a1
                ax.axvline(x=x)
        for x, y in factibles:
            ax.plot(x, y, 'bo')
        x_opt, y_opt = optimo
        ax.plot(x_opt, y_opt, 'ro', label='Óptimo')
        ax.text(x_opt + 0.5, y_opt, f'({x_opt:.2f}, {y_opt:.2f})', color='red')
        ax.set_xlabel("x₁")
        ax.set_ylabel("x₂")
        ax.grid(True)
        ax.legend()
        plt.title("Solución Gráfica del PL")
        plt.show()

# Ejecutar app
if __name__ == "__main__":
    root = tk.Tk()
    app = SolverPL(root)
    root.mainloop()
