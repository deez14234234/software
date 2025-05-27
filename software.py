import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import matplotlib.patches as patches

class ModernSolverPL:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Solucionador de Programación Lineal")
        
        # Configurar ventana principal
        ancho, alto = 1000, 700
        self.root.geometry(f"{ancho}x{alto}")
        self.root.resizable(True, True)
        
        # Centrar ventana
        x_centro = int(self.root.winfo_screenwidth() / 2 - ancho / 2)
        y_centro = int(self.root.winfo_screenheight() / 2 - alto / 2)
        self.root.geometry(f"+{x_centro}+{y_centro}")
        
        # Configurar estilo moderno
        self.configurar_estilos()
        
        # Variables
        self.tipo_var = tk.StringVar(value="Maximización")
        self.num_restr_var = tk.IntVar(value=2)
        
        # Crear interfaz
        self.crear_interfaz_moderna()
        
    def configurar_estilos(self):
        """Configurar estilos modernos para la aplicación"""
        self.root.configure(bg="#f8fafc")
        
        # Configurar ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones
        style.configure("Modern.TButton",
                       background="#4f46e5",
                       foreground="white",
                       font=("Inter", 10, "bold"),
                       borderwidth=0,
                       focuscolor="none")
        
        style.map("Modern.TButton",
                 background=[('active', '#4338ca'), ('disabled', '#9ca3af')])
        
        # Estilo para botón resolver
        style.configure("Solve.TButton",
                       background="#10b981",
                       foreground="white",
                       font=("Inter", 12, "bold"),
                       borderwidth=0,
                       focuscolor="none")
        
        style.map("Solve.TButton",
                 background=[('active', '#059669')])
        
        # Estilo para combobox
        style.configure("Modern.TCombobox",
                       fieldbackground="white",
                       background="white",
                       borderwidth=2,
                       relief="solid")
        
        # Estilo para entry
        style.configure("Modern.TEntry",
                       fieldbackground="white",
                       borderwidth=2,
                       relief="solid")
        
    def crear_interfaz_moderna(self):
        """Crear la interfaz moderna principal"""
        # Header principal
        self.crear_header()
        
        # Contenedor principal con grid
        main_container = tk.Frame(self.root, bg="#f8fafc")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Panel izquierdo (controles)
        self.crear_panel_izquierdo(main_container)
        
        # Panel derecho (resultados)
        self.crear_panel_derecho(main_container)
        
        # Generar formulario inicial
        self.generar_formulario()
        
    def crear_header(self):
        """Crear header moderno con gradiente simulado"""
        header_frame = tk.Frame(self.root, bg="#4f46e5", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Título principal
        title_label = tk.Label(header_frame, 
                              text="🔍 Solucionador de Programación Lineal",
                              font=("Inter", 20, "bold"),
                              bg="#4f46e5", fg="white")
        title_label.pack(pady=15)
        
        # Subtítulo
        subtitle_label = tk.Label(header_frame,
                                 text="Encuentra la solución óptima de manera visual e intuitiva",
                                 font=("Inter", 11),
                                 bg="#4f46e5", fg="#e0e7ff")
        subtitle_label.pack()
        
    def crear_panel_izquierdo(self, parent):
        """Crear panel izquierdo con controles"""
        self.left_panel = tk.Frame(parent, bg="#f8fafc")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Configuración del problema
        self.crear_card_configuracion()
        
        # Función objetivo
        self.crear_card_objetivo()
        
        # Restricciones
        self.crear_card_restricciones()
        
        # Botón resolver
        self.crear_boton_resolver()
        
    def crear_panel_derecho(self, parent):
        """Crear panel derecho con resultados"""
        self.right_panel = tk.Frame(parent, bg="#f8fafc")
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        # Card de resultados
        self.crear_card_resultados()
        
        # Card de gráfico (placeholder)
        self.crear_card_grafico()
        
    def crear_card_configuracion(self):
        """Crear card de configuración del problema"""
        card = self.crear_card_base(self.left_panel, "⚙️ Configuración del Problema")
        
        # Tipo de problema
        tipo_frame = tk.Frame(card, bg="white")
        tipo_frame.pack(fill="x", pady=5)
        
        tk.Label(tipo_frame, text="Tipo de optimización:", 
                font=("Inter", 10), bg="white").pack(side="left", padx=5)
        
        tipo_combo = ttk.Combobox(tipo_frame, textvariable=self.tipo_var,
                                 values=["Maximización", "Minimización"],
                                 state="readonly", width=15, style="Modern.TCombobox")
        tipo_combo.pack(side="left", padx=5)
        
        # Número de restricciones
        restr_frame = tk.Frame(card, bg="white")
        restr_frame.pack(fill="x", pady=5)
        
        tk.Label(restr_frame, text="Número de restricciones:",
                font=("Inter", 10), bg="white").pack(side="left", padx=5)
        
        # Botones para cambiar restricciones
        btn_frame = tk.Frame(restr_frame, bg="white")
        btn_frame.pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="−", width=3,
                  command=lambda: self.cambiar_restricciones(-1),
                  style="Modern.TButton").pack(side="left")
        
        self.label_restr = tk.Label(btn_frame, text="2", 
                                   font=("Inter", 10, "bold"),
                                   bg="#f1f5f9", fg="#475569",
                                   width=3, relief="solid", bd=1)
        self.label_restr.pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="+", width=3,
                  command=lambda: self.cambiar_restricciones(1),
                  style="Modern.TButton").pack(side="left")
        
    def crear_card_objetivo(self):
        """Crear card de función objetivo"""
        self.obj_card = self.crear_card_base(self.left_panel, "🎯 Función Objetivo")
        
    def crear_card_restricciones(self):
        """Crear card de restricciones"""
        self.rest_card = self.crear_card_base(self.left_panel, "📐 Restricciones")
        
    def crear_card_base(self, parent, titulo):
        """Crear una card base con estilo moderno"""
        # Frame principal de la card
        card_frame = tk.Frame(parent, bg="#f8fafc")
        card_frame.pack(fill="x", pady=10)
        
        # Card container
        card = tk.Frame(card_frame, bg="white", relief="solid", bd=1)
        card.pack(fill="x", padx=2, pady=2)
        
        # Título de la card
        title_frame = tk.Frame(card, bg="white")
        title_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        tk.Label(title_frame, text=titulo, 
                font=("Inter", 12, "bold"), 
                bg="white", fg="#1f2937").pack(side="left")
        
        # Contenido de la card
        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        return content_frame
        
    def crear_boton_resolver(self):
        """Crear botón resolver con estilo moderno"""
        btn_frame = tk.Frame(self.left_panel, bg="#f8fafc")
        btn_frame.pack(fill="x", pady=20)
        
        solve_btn = ttk.Button(btn_frame, text="🚀 Resolver Problema",
                              command=self.resolver,
                              style="Solve.TButton")
        solve_btn.pack(pady=10)
        
    def crear_card_resultados(self):
        """Crear card de resultados"""
        card = self.crear_card_base(self.right_panel, "📊 Resultado Óptimo")
        
        # Contenedor de resultados
        self.result_frame = tk.Frame(card, bg="#f0f9ff", relief="solid", bd=1)
        self.result_frame.pack(fill="both", expand=True, pady=10)
        
        # Texto inicial
        self.result_label = tk.Label(self.result_frame, 
                                    text="Ingresa los datos y presiona\n'Resolver' para ver la solución",
                                    font=("Inter", 11),
                                    bg="#f0f9ff", fg="#0f172a",
                                    justify="center")
        self.result_label.pack(expand=True)
        
    def crear_card_grafico(self):
        """Crear card placeholder para gráfico"""
        card = self.crear_card_base(self.right_panel, "📈 Visualización Gráfica")
        
        self.chart_frame = tk.Frame(card, bg="#f8fafc", relief="solid", bd=1, height=200)
        self.chart_frame.pack(fill="both", expand=True, pady=10)
        self.chart_frame.pack_propagate(False)
        
        tk.Label(self.chart_frame, 
                text="El gráfico aparecerá en una ventana separada\ndespués de resolver el problema",
                font=("Inter", 10),
                bg="#f8fafc", fg="#64748b",
                justify="center").pack(expand=True)
        
    def cambiar_restricciones(self, delta):
        """Cambiar número de restricciones"""
        nuevo_valor = max(1, min(5, self.num_restr_var.get() + delta))
        self.num_restr_var.set(nuevo_valor)
        self.label_restr.config(text=str(nuevo_valor))
        self.generar_formulario()
        
    def generar_formulario(self):
        """Generar formulario dinámico"""
        # Limpiar contenido anterior
        for widget in self.obj_card.winfo_children():
            widget.destroy()
        for widget in self.rest_card.winfo_children():
            widget.destroy()
            
        self.generar_funcion_objetivo()
        self.generar_restricciones()
        
    def generar_funcion_objetivo(self):
        """Generar campos de función objetivo"""
        self.sign_vars = []
        self.c_vars = []
        
        for i in range(2):
            row_frame = self.crear_fila_moderna(self.obj_card)
            
            # Signo
            sign = ttk.Combobox(row_frame, values=["+", "−"], width=3,
                               state="readonly", style="Modern.TCombobox")
            sign.set("+")
            sign.pack(side="left", padx=2)
            
            # Coeficiente
            coef = ttk.Entry(row_frame, width=8, style="Modern.TEntry")
            coef.insert(0, "1")
            coef.pack(side="left", padx=2)
            
            # Variable
            tk.Label(row_frame, text=f"x₁" if i == 0 else f"x₂",
                    font=("Inter", 10, "bold"), bg="#f8fafc", fg="#4f46e5").pack(side="left", padx=2)
            
            self.sign_vars.append(sign)
            self.c_vars.append(coef)
            
    def generar_restricciones(self):
        """Generar campos de restricciones"""
        self.a_vars, self.signos, self.b_vars = [], [], []
        
        for i in range(self.num_restr_var.get()):
            row_frame = self.crear_fila_moderna(self.rest_card)
            
            # Coeficientes
            fila_vars = []
            for j in range(2):
                coef = ttk.Entry(row_frame, width=6, style="Modern.TEntry")
                coef.insert(0, "1")
                coef.pack(side="left", padx=2)
                
                tk.Label(row_frame, text=f"x₁" if j == 0 else f"x₂",
                        font=("Inter", 9, "bold"), bg="#f8fafc", fg="#4f46e5").pack(side="left", padx=1)
                
                if j == 0:
                    tk.Label(row_frame, text="+", bg="#f8fafc").pack(side="left", padx=2)
                
                fila_vars.append(coef)
            
            self.a_vars.append(fila_vars)
            
            # Operador
            signo = ttk.Combobox(row_frame, values=["≤", "≥", "="], width=4,
                                state="readonly", style="Modern.TCombobox")
            signo.set("≤")
            signo.pack(side="left", padx=5)
            self.signos.append(signo)
            
            # Valor derecho
            b = ttk.Entry(row_frame, width=6, style="Modern.TEntry")
            b.insert(0, "1")
            b.pack(side="left", padx=2)
            self.b_vars.append(b)
            
    def crear_fila_moderna(self, parent):
        """Crear una fila con estilo moderno"""
        row_frame = tk.Frame(parent, bg="#f8fafc", relief="solid", bd=1)
        row_frame.pack(fill="x", pady=5, padx=5)
        
        # Padding interno
        inner_frame = tk.Frame(row_frame, bg="#f8fafc")
        inner_frame.pack(padx=10, pady=8)
        
        return inner_frame
        
    def mostrar_notificacion(self, titulo, mensaje, tipo="info"):
        """Mostrar notificación moderna"""
        if tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "success":
            messagebox.showinfo(titulo, mensaje)
        else:
            messagebox.showinfo(titulo, mensaje)
            
    def resolver(self):
        """Resolver el problema de programación lineal"""
        try:
            # Obtener datos
            tipo = self.tipo_var.get()
            c = []
            
            for i in range(2):
                sign = 1 if self.sign_vars[i].get() == "+" else -1
                coef = float(self.c_vars[i].get() or 0)
                c.append(sign * coef)
            
            # Obtener restricciones
            A, b, signos = [], [], []
            for i in range(self.num_restr_var.get()):
                fila = []
                for j in range(2):
                    val = float(self.a_vars[i][j].get() or 0)
                    fila.append(val)
                A.append(fila)
                b.append(float(self.b_vars[i].get() or 0))
                
                # Convertir símbolos
                signo_texto = self.signos[i].get()
                if signo_texto == "≤":
                    signos.append("<=")
                elif signo_texto == "≥":
                    signos.append(">=")
                else:
                    signos.append("=")
            
            # Normalizar restricciones
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
            
            # Resolver
            resultado = self.resolver_pl(c, norm_rest, tipo)
            
            if resultado:
                # Mostrar resultado
                self.mostrar_resultado(resultado, tipo)
                
                # Mostrar gráfico
                self.graficar_moderna(norm_rest, resultado['factibles'], resultado['optimo'])
                
                self.mostrar_notificacion("¡Éxito!", "Problema resuelto exitosamente", "success")
            else:
                self.mostrar_notificacion("Sin solución", "No hay solución factible", "error")
                
        except Exception as e:
            self.mostrar_notificacion("Error", f"Ocurrió un error: {str(e)}", "error")
            
    def resolver_pl(self, c, restricciones, tipo):
        """Lógica de resolución del problema lineal"""
        def intersec(r1, r2):
            a1, a2, b1 = r1
            c1, c2, b2 = r2
            det = a1*c2 - c1*a2
            if abs(det) < 1e-10:
                return None
            x = (b1*c2 - b2*a2) / det
            y = (a1*b2 - c1*b1) / det
            return [x, y]
        
        # Encontrar puntos candidatos
        puntos = [[0, 0]]
        
        # Intersecciones con ejes
        for a1, a2, b_ in restricciones:
            if abs(a2) > 1e-10:
                puntos.append([0, b_/a2])
            if abs(a1) > 1e-10:
                puntos.append([b_/a1, 0])
        
        # Intersecciones entre restricciones
        for i in range(len(restricciones)):
            for j in range(i+1, len(restricciones)):
                p = intersec(restricciones[i], restricciones[j])
                if p:
                    puntos.append(p)
        
        # Filtrar puntos factibles
        factibles = []
        for x, y in puntos:
            if x < -1e-6 or y < -1e-6:
                continue
            if all(a1*x + a2*y <= b_ + 1e-6 for a1, a2, b_ in restricciones):
                factibles.append([max(0, x), max(0, y)])
        
        if not factibles:
            return None
        
        # Evaluar función objetivo
        soluciones = []
        for p in factibles:
            z = c[0]*p[0] + c[1]*p[1]
            soluciones.append({"punto": p, "z": z})
        
        # Encontrar óptimo
        if tipo == "Maximización":
            optimo = max(soluciones, key=lambda d: d["z"])
        else:
            optimo = min(soluciones, key=lambda d: d["z"])
        
        return {
            'optimo': optimo["punto"],
            'valor_z': optimo["z"],
            'factibles': factibles
        }
    
    def mostrar_resultado(self, resultado, tipo):
        """Mostrar resultado en la interfaz"""
        # Limpiar frame anterior
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Cambiar color de fondo
        self.result_frame.config(bg="white")
        
        # Valor de Z
        z_frame = tk.Frame(self.result_frame, bg="white")
        z_frame.pack(pady=10)
        
        tk.Label(z_frame, text=f"Z = {resultado['valor_z']:.3f}",
                font=("Inter", 18, "bold"), bg="white", fg="#0ea5e9").pack()
        
        # Valores de variables
        vars_frame = tk.Frame(self.result_frame, bg="white")
        vars_frame.pack(pady=5)
        
        x1, x2 = resultado['optimo']
        tk.Label(vars_frame, text=f"x₁ = {x1:.3f}",
                font=("Inter", 12), bg="white").pack()
        tk.Label(vars_frame, text=f"x₂ = {x2:.3f}",
                font=("Inter", 12), bg="white").pack()
        
        # Tipo de valor
        tipo_texto = "Máximo" if tipo == "Maximización" else "Mínimo"
        tk.Label(self.result_frame, text=f"Valor {tipo_texto}",
                font=("Inter", 10), bg="white", fg="#64748b").pack(pady=(10, 0))
        
    def graficar_moderna(self, restricciones, factibles, optimo):
        """Crear gráfico moderno con matplotlib"""
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor('#f8fafc')
        ax.set_facecolor('white')
        
        # Configurar límites del gráfico
        max_val = max(20, optimo[0] * 1.5, optimo[1] * 1.5)
        x_vals = np.linspace(0, max_val, 400)
        
        # Colores modernos
        colors = ['#4f46e5', '#7c3aed', '#06b6d4', '#10b981', '#f59e0b']
        
        # Dibujar restricciones
        for idx, (a1, a2, b) in enumerate(restricciones):
            color = colors[idx % len(colors)]
            if abs(a2) > 1e-10:
                y_vals = (b - a1 * x_vals) / a2
                y_vals = np.clip(y_vals, 0, max_val)
                ax.plot(x_vals, y_vals, color=color, linewidth=2.5,
                       label=f'{a1:.0f}x₁ + {a2:.0f}x₂ ≤ {b:.0f}')
            elif abs(a1) > 1e-10:
                x_line = b / a1
                if 0 <= x_line <= max_val:
                    ax.axvline(x=x_line, color=color, linewidth=2.5,
                              label=f'x₁ = {x_line:.1f}')
        
        # Dibujar región factible
        if len(factibles) >= 3:
            # Ordenar puntos para formar polígono convexo
            from scipy.spatial import ConvexHull
            try:
                hull = ConvexHull(factibles)
                hull_points = [factibles[i] for i in hull.vertices]
                poligono = Polygon(hull_points, closed=True, 
                                 facecolor='#10b981', alpha=0.2, 
                                 edgecolor='#059669', linewidth=2)
                ax.add_patch(poligono)
            except:
                # Fallback si scipy no está disponible
                factibles_ordenados = sorted(factibles, 
                    key=lambda p: np.arctan2(p[1] - optimo[1], p[0] - optimo[0]))
                poligono = Polygon(factibles_ordenados, closed=True,
                                 facecolor='#10b981', alpha=0.2,
                                 edgecolor='#059669', linewidth=2)
                ax.add_patch(poligono)
        
        # Dibujar puntos factibles
        if factibles:
            x_coords, y_coords = zip(*factibles)
            ax.scatter(x_coords, y_coords, c='#3b82f6', s=60, 
                      zorder=5, alpha=0.7, label='Puntos factibles')
        
        # Dibujar punto óptimo
        x_opt, y_opt = optimo
        ax.scatter(x_opt, y_opt, c='#ef4444', s=120, zorder=10,
                  marker='*', label='Punto óptimo')
        ax.annotate(f'({x_opt:.2f}, {y_opt:.2f})', 
                   (x_opt, y_opt), xytext=(10, 10), 
                   textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='#fef2f2', 
                            edgecolor='#ef4444'),
                   fontsize=10, fontweight='bold')
        
        # Configurar ejes y grid
        ax.set_xlabel("x₁", fontsize=12, fontweight='bold')
        ax.set_ylabel("x₂", fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax.set_xlim(0, max_val)
        ax.set_ylim(0, max_val)
        
        # Configurar leyenda
        ax.legend(loc='upper right', frameon=True, fancybox=True, 
                 shadow=True, fontsize=10)
        
        # Título
        plt.title("📈 Solución Gráfica del Problema de Programación Lineal", 
                 fontsize=14, fontweight='bold', pad=20)
        
        # Mejorar apariencia
        plt.tight_layout()
        plt.show()

# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernSolverPL(root)
    root.mainloop()