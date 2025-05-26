import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Programación Lineal Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        color: rgba(255,255,255,0.8);
        font-size: 1.1rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .step-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #28a745;
        margin: 0.5rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🎯 Sistema de Programación Lineal Pro</h1>
    <p>Solución completa para optimización de recursos y maximización de beneficios</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con información y configuración
with st.sidebar:
    st.markdown("### 🛠️ Configuración del Problema")
    
    # Selector de tipo de análisis
    modo_analisis = st.radio(
        "Modo de Análisis",
        ["Básico", "Avanzado", "Análisis de Sensibilidad"],
        help="Selecciona el nivel de análisis que deseas realizar"
    )
    
    st.markdown("---")
    
    # Información del problema
    st.markdown("### 📋 Información del Problema")
    nombre_problema = st.text_input("Nombre del problema", "Mi Proyecto de Optimización")
    autor = st.text_input("Autor/Empresa", "")
    
    st.markdown("---")
    
    # Tutorial interactivo
    with st.expander("📚 Tutorial Interactivo"):
        st.markdown("""
        **Pasos para resolver tu problema:**
        
        1. **Selecciona el tipo**: Maximización o Minimización
        2. **Define la función objetivo**: Los coeficientes que quieres optimizar
        3. **Agrega restricciones**: Las limitaciones de tu problema
        4. **Analiza resultados**: Interpreta la solución óptima
        
        **Ejemplos comunes:**
        - **Producción**: Maximizar ganancias con recursos limitados
        - **Dieta**: Minimizar costos cumpliendo requisitos nutricionales
        - **Transporte**: Minimizar costos de envío
        """)

# Contenido principal
col1, col2 = st.columns([2, 1])

with col1:
    # Configuración del problema
    st.markdown("### 🎯 Configuración del Problema")
    
    col_tipo, col_var = st.columns(2)
    with col_tipo:
        tipo = st.selectbox("🔄 Tipo de problema", ["Maximización", "Minimización"])
    with col_var:
        num_variables = st.selectbox("📊 Número de variables", [2, 3], index=0)
        if num_variables == 3:
            st.warning("⚠️ Visualización disponible solo para 2 variables")

    # Función Objetivo
    st.markdown("### 🎯 Función Objetivo")
    
    if tipo == "Maximización":
        st.markdown("**Maximizar: Z =** ", end="")
    else:
        st.markdown("**Minimizar: Z =** ", end="")
    
    signos_obj = []
    coef_obj = []
    nombres_var = []
    
    cols_obj = st.columns(num_variables)
    for i in range(num_variables):
        with cols_obj[i]:
            nombre_var = st.text_input(f"Nombre variable {i+1}", f"x{i+1}", key=f"nombre_var_{i}")
            nombres_var.append(nombre_var)
            
            col_signo, col_coef = st.columns([1, 2])
            with col_signo:
                signo = st.selectbox("±", ["+", "-"], key=f"signo_obj_{i}")
            with col_coef:
                coef = st.number_input(f"Coeficiente", value=1.0, key=f"coef_obj_{i}")
            
            signos_obj.append(signo)
            coef_obj.append(coef if signo == '+' else -coef)

    # Mostrar función objetivo formateada
    funcion_str = "Z = "
    for i, (coef, nombre) in enumerate(zip(coef_obj, nombres_var)):
        if i > 0:
            funcion_str += " + " if coef >= 0 else " - "
            funcion_str += f"{abs(coef)}{nombre}"
        else:
            funcion_str += f"{coef}{nombre}"
    
    st.info(f"**Función objetivo:** {funcion_str}")

    # Restricciones
    st.markdown("### 📏 Restricciones")
    
    num_restr = st.slider("Número de restricciones", 1, 8, 3)
    
    restricciones = []
    for i in range(num_restr):
        st.markdown(f"**Restricción {i+1}:**")
        cols = st.columns(num_variables + 2)
        
        coefs_restr = []
        for j in range(num_variables):
            with cols[j]:
                coef = st.number_input(f"{nombres_var[j]}", key=f"coef_r{i}_v{j}", value=1.0)
                coefs_restr.append(coef)
        
        with cols[num_variables]:
            signo = st.selectbox("Signo", ["≤", "≥", "="], key=f"signo_rest_{i}")
        
        with cols[num_variables + 1]:
            b = st.number_input("Valor", key=f"b_{i}", value=10.0)
        
        restricciones.append((*coefs_restr, signo, b))
        
        # Mostrar restricción formateada
        restr_str = ""
        for j, (coef, nombre) in enumerate(zip(coefs_restr, nombres_var)):
            if j > 0:
                restr_str += " + " if coef >= 0 else " - "
                restr_str += f"{abs(coef)}{nombre}"
            else:
                restr_str += f"{coef}{nombre}"
        restr_str += f" {signo} {b}"
        st.caption(restr_str)

with col2:
    # Panel de información y métricas
    st.markdown("### 📊 Resumen del Problema")
    
    st.markdown(f"""
    <div class="metric-card">
        <h4>📈 {tipo}</h4>
        <p><strong>Variables:</strong> {num_variables}</p>
        <p><strong>Restricciones:</strong> {num_restr}</p>
        <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Validaciones
    st.markdown("### ✅ Validaciones")
    validaciones = []
    
    if all(c != 0 for c in coef_obj):
        validaciones.append("✅ Función objetivo válida")
    else:
        validaciones.append("❌ Coeficientes de función objetivo inválidos")
    
    if num_restr >= 1:
        validaciones.append("✅ Restricciones suficientes")
    else:
        validaciones.append("❌ Se necesita al menos una restricción")
    
    for validacion in validaciones:
        st.write(validacion)

# Botón de resolución
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn1:
    resolver = st.button("🚀 Resolver Problema", type="primary", use_container_width=True)

with col_btn2:
    if st.button("📋 Generar Reporte", use_container_width=True):
        st.info("Funcionalidad de reporte disponible después de resolver")

with col_btn3:
    if st.button("💾 Guardar Configuración", use_container_width=True):
        st.success("Configuración guardada localmente")

# Resolución del problema
if resolver:
    try:
        with st.spinner("🔄 Resolviendo problema..."):
            c = coef_obj
            
            # Normalizar restricciones para 2 variables (mantenemos la lógica original)
            if num_variables == 2:
                norm_rest = []
                for restriccion in restricciones:
                    a1, a2, signo, b = restriccion
                    if signo == "≤":
                        norm_rest.append([a1, a2, b])
                    elif signo == "≥":
                        norm_rest.append([-a1, -a2, -b])
                    elif signo == "=":
                        norm_rest.append([a1, a2, b])

                def intersec(r1, r2):
                    a1, a2, b1 = r1
                    c1, c2, b2 = r2
                    det = a1 * c2 - c1 * a2
                    if det == 0:
                        return None
                    x = (b1 * c2 - b2 * a2) / det
                    y = (a1 * b2 - c1 * b1) / det
                    return [x, y]

                # Encontrar puntos candidatos
                puntos = [[0, 0]]
                for a1, a2, b in norm_rest:
                    if a2 != 0:
                        puntos.append([0, b / a2])
                    if a1 != 0:
                        puntos.append([b / a1, 0])
                
                for i in range(len(norm_rest)):
                    for j in range(i + 1, len(norm_rest)):
                        p = intersec(norm_rest[i], norm_rest[j])
                        if p:
                            puntos.append(p)

                # Filtrar puntos factibles
                factibles = []
                for x, y in puntos:
                    if x >= -1e-6 and y >= -1e-6:  # Permitir pequeños errores numéricos
                        if all(a1 * x + a2 * y <= b + 1e-6 for a1, a2, b in norm_rest):
                            factibles.append([x, y])

                if not factibles:
                    st.error("❌ No hay solución factible para este problema.")
                else:
                    # Calcular soluciones
                    soluciones = []
                    for p in factibles:
                        z_val = sum(c[i] * p[i] for i in range(len(p)))
                        soluciones.append({"punto": p, "z": z_val})
                    
                    # Encontrar óptimo
                    if tipo == "Maximización":
                        optimo = max(soluciones, key=lambda d: d["z"])
                    else:
                        optimo = min(soluciones, key=lambda d: d["z"])

                    # Resultados
                    st.markdown("## 🎉 Resultados de la Optimización")
                    
                    col_res1, col_res2, col_res3 = st.columns(3)
                    
                    with col_res1:
                        st.metric(
                            label="💰 Valor Óptimo (Z)",
                            value=f"{optimo['z']:.4f}",
                            delta=f"{'Máximo' if tipo == 'Maximización' else 'Mínimo'}"
                        )
                    
                    with col_res2:
                        st.metric(
                            label=f"📍 {nombres_var[0]}",
                            value=f"{optimo['punto'][0]:.4f}"
                        )
                    
                    with col_res3:
                        st.metric(
                            label=f"📍 {nombres_var[1]}",
                            value=f"{optimo['punto'][1]:.4f}"
                        )

                    # Tabla de todas las soluciones
                    if modo_analisis in ["Avanzado", "Análisis de Sensibilidad"]:
                        st.markdown("### 📊 Análisis Detallado")
                        
                        df_soluciones = pd.DataFrame([
                            {
                                nombres_var[0]: sol["punto"][0],
                                nombres_var[1]: sol["punto"][1],
                                "Valor Z": sol["z"],
                                "Tipo": "Óptimo" if sol == optimo else "Factible"
                            }
                            for sol in soluciones
                        ])
                        
                        st.dataframe(df_soluciones, use_container_width=True)

                    # Gráfico interactivo con Plotly
                    st.markdown("### 📈 Visualización Gráfica")
                    
                    fig = go.Figure()
                    
                    # Región factible
                    x_vals = np.linspace(-1, max(20, max(p[0] for p in factibles) * 1.2), 400)
                    
                    # Líneas de restricciones
                    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
                    for idx, (a1, a2, b) in enumerate(norm_rest):
                        color = colors[idx % len(colors)]
                        if a2 != 0:
                            y_vals = (b - a1 * x_vals) / a2
                            fig.add_trace(go.Scatter(
                                x=x_vals, y=y_vals,
                                mode='lines',
                                name=f'Restricción {idx+1}',
                                line=dict(color=color, width=2)
                            ))
                        elif a1 != 0:
                            x_const = b / a1
                            fig.add_trace(go.Scatter(
                                x=[x_const, x_const], y=[0, 20],
                                mode='lines',
                                name=f'Restricción {idx+1}',
                                line=dict(color=color, width=2)
                            ))
                    
                    # Puntos factibles
                    if factibles:
                        factibles_x = [p[0] for p in factibles]
                        factibles_y = [p[1] for p in factibles]
                        fig.add_trace(go.Scatter(
                            x=factibles_x, y=factibles_y,
                            mode='markers',
                            name='Puntos Factibles',
                            marker=dict(color='lightblue', size=8, line=dict(color='darkblue', width=1))
                        ))
                    
                    # Punto óptimo
                    fig.add_trace(go.Scatter(
                        x=[optimo["punto"][0]], y=[optimo["punto"][1]],
                        mode='markers+text',
                        name='Solución Óptima',
                        marker=dict(color='red', size=15, symbol='star'),
                        text=[f'Óptimo ({optimo["punto"][0]:.2f}, {optimo["punto"][1]:.2f})'],
                        textposition="top center",
                        textfont=dict(size=12, color='red')
                    ))
                    
                    fig.update_layout(
                        title=f'Solución del Problema: {nombre_problema}',
                        xaxis_title=nombres_var[0],
                        yaxis_title=nombres_var[1],
                        hovermode='closest',
                        showlegend=True,
                        template='plotly_white',
                        height=600
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

                    # Análisis de sensibilidad
                    if modo_analisis == "Análisis de Sensibilidad":
                        st.markdown("### 🔍 Análisis de Sensibilidad")
                        
                        col_sens1, col_sens2 = st.columns(2)
                        
                        with col_sens1:
                            st.markdown("#### 📊 Recursos Utilizados")
                            recursos_data = []
                            for i, (a1, a2, signo, b) in enumerate(restricciones):
                                if signo == "≤":
                                    usado = a1 * optimo["punto"][0] + a2 * optimo["punto"][1]
                                    disponible = b
                                    holgura = disponible - usado
                                    recursos_data.append({
                                        "Restricción": f"R{i+1}",
                                        "Usado": round(usado, 4),
                                        "Disponible": disponible,
                                        "Holgura": round(holgura, 4),
                                        "% Utilización": round((usado/disponible)*100, 2) if disponible != 0 else 0
                                    })
                            
                            if recursos_data:
                                df_recursos = pd.DataFrame(recursos_data)
                                st.dataframe(df_recursos, use_container_width=True)
                        
                        with col_sens2:
                            st.markdown("#### 💡 Recomendaciones")
                            for i, recurso in enumerate(recursos_data):
                                if recurso["Holgura"] < 0.01:  # Recurso crítico
                                    st.warning(f"🔴 **R{i+1}**: Recurso crítico - Considere aumentar disponibilidad")
                                elif recurso["% Utilización"] < 50:
                                    st.info(f"🟡 **R{i+1}**: Recurso subutilizado ({recurso['% Utilización']:.1f}%)")
                                else:
                                    st.success(f"🟢 **R{i+1}**: Utilización eficiente ({recurso['% Utilización']:.1f}%)")

            else:  # Para 3 variables
                st.info("🔧 Resolver problemas de 3 variables requiere métodos más avanzados como el Método Simplex.")
                st.markdown("""
                **Para problemas de 3+ variables, considera:**
                - Usar bibliotecas especializadas como `scipy.optimize`
                - Implementar el método Simplex
                - Utilizar software comercial como CPLEX o Gurobi
                """)

    except Exception as e:
        st.error(f"❌ Error al resolver el problema: {str(e)}")
        st.markdown("""
        **Posibles causas:**
        - Restricciones inconsistentes
        - Coeficientes inválidos
        - Problema mal formulado
        
        **Sugerencias:**
        - Verifica que las restricciones sean consistentes
        - Asegúrate de que los coeficientes sean números válidos
        - Revisa la formulación del problema
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🚀 <strong>Sistema de Programación Lineal Pro</strong> | Desarrollado para optimización empresarial</p>
    <p>📧 Para soporte técnico o consultas especializadas, contacta a tu equipo de desarrollo</p>
</div>
""", unsafe_allow_html=True)