# app principal mejorado para el cálculo de tiempos semafóricos vehicular y peatonal
import streamlit as st
from funcion_webster import (
    calcular_cargas, calcular_tiempo_total_perdido, calcular_ciclo_webster,
    calcular_verdes, calcular_verde_real, verificar_tiempo_rojo, ajustar_tiempos
)
from funcion_diagramas2 import graficar_fases, graficar_fases_peatonal

# =======================
# CONFIGURACIÓN INICIAL
# =======================
st.set_page_config(page_title="🚦 Tiempos Semafóricos - Método de Webster", layout="wide")
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }
        h1, h3 {
            font-family: 'Arial';
        }
        .centered {
            text-align: center;
        }
        .stButton>button {
            background-color: #004d99;
            color: white;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# =======================
# TÍTULO Y DESCRIPCIÓN
# =======================
st.markdown("""
    <h1 class='centered' style='color: #004d99;'>🚦 Cálculo de Tiempos Semafóricos Vehicular y Peatonal</h1>
    <h3 class='centered' style='color: gray;'>📐 Desarrollado en base al Método Determinístico de Webster</h3>
    <hr style='border: 1px solid #e0e0e0;'>
""", unsafe_allow_html=True)

# =======================
# 1. PARÁMETROS DE ENTRADA
# =======================
st.header("🧮 1. Parámetros de Entrada")
with st.expander("📥 Ingreso de Flujos y Capacidades", expanded=True):
    st.subheader("🚗 Flujos Vehiculares directos equivalentes (ucpd/h) o Automoviles directos equivalentes(ADE/h)")
    col1, col2 = st.columns(2)
    with col1:
        q = {
            'norte': st.number_input('➡️ Norte:', value=600, min_value=0),
            'sur':   st.number_input('⬅️ Sur:', value=400, min_value=0)
        }
    with col2:
        q.update({
            'este':  st.number_input('⬆️ Este:', value=750, min_value=0),
            'oeste': st.number_input('⬇️ Oeste:', value=1200, min_value=0)
        })

    st.subheader(" 📊 Flujos de Saturación ")
    col1, col2 = st.columns(2)
    with col1:
        S = {
            'norte': st.number_input('➡️ Flujos de Saturación Norte:', value=2400, min_value=1),
            'sur':   st.number_input('⬅️ Flujos de Saturación Sur:', value=2000, min_value=1)
        }
    with col2:
        S.update({
            'este':  st.number_input('⬆️ Flujos de Saturación Este:', value=3000, min_value=1),
            'oeste': st.number_input('⬇️ Flujos de Saturación Oeste:', value=3000, min_value=1)
        })

st.markdown("### ⚙️ Parámetros del Ciclo Semafórico")
col1, col2, col3 = st.columns(3)
with col1:
    TR = st.number_input('⏱️ Tiempo Todo Rojo (s):', value=4, min_value=0)
with col2:
    tp = st.number_input('⏱️ Tiempo Perdido por Fase (s):', value=2, min_value=0)
with col3:
    ta = st.number_input('⏱️ Tiempo Ámbar (s):', value=3, min_value=0)

# Tiempo peatonal
tc = st.slider("🚶‍♂️ Tiempo de Cruce Peatonal (s)", 3.0, 50.0, 35.71, step=1.0)

# =======================
# 2. EJECUCIÓN DE CÁLCULOS
# =======================
st.markdown("---")
if st.button("📊 Calcular Ciclo y Tiempos", use_container_width=True):
    try:
        with st.spinner("🔄 Calculando ciclo y tiempos óptimos..."):
            num_fases = 2
            ye, yp_1, yp_2, Y = calcular_cargas(q, S)
            T = calcular_tiempo_total_perdido(num_fases, TR, tp)
            C = calcular_ciclo_webster(T, Y)
            _, v1, v2 = calcular_verdes(C, T, yp_1, yp_2, Y)
            v1_real, v2_real = calcular_verde_real(v1, v2, tp, ta)
            rojo = lambda ciclo, verde: ciclo - verde - ta - TR
            rojo_EO = rojo(C, v1_real)
            rojo_NS = rojo(C, v2_real)

        st.toast("✅ Cálculo completado exitosamente")

        # =======================
        # RESULTADOS
        # =======================
        with st.container():
            st.subheader("📈 2. Resultados Iniciales - 2 Fases")
            with st.expander("📋 Parámetros Calculados"):
                st.markdown(f"- **Carga direccional (ye):** {ye}")
                st.markdown(f"- **Carga por fase:** yp₁ = {yp_1:.3f}, yp₂ = {yp_2:.3f}")
                st.markdown(f"- **Carga total (Y):** {Y:.3f}")
                st.markdown(f"- ⏱️ **Ciclo óptimo:** {C:.2f} s")
                st.markdown(f"- 🟩 **Verde real E-O:** {v1_real:.2f} s")
                st.markdown(f"- 🟩 **Verde real N-S:** {v2_real:.2f} s")
                st.markdown(f"- 🔴 **Rojo E-O:** {rojo_EO:.2f} s")
                st.markdown(f"- 🔴 **Rojo N-S:** {rojo_NS:.2f} s")

        st.subheader("🚗 Diagrama de Fases Vehiculares")
        st.pyplot(graficar_fases(C, v1_real, v2_real, ta, TR))

        # =======================
        # VERIFICACIÓN PEATONAL
        # =======================
        st.subheader("🚶‍♂️ Verificación del Cruce Peatonal")
        with st.expander("📋 Tiempo Disponible vs Requerido"):
            rojo_I_fase_EO = rojo_EO + TR
            rojo_II_fase_NS = rojo_NS + TR
            st.markdown(f"- 🔴 **Rojo E-O:** {rojo_I_fase_EO:.2f} s")
            st.markdown(f"- 🔴 **Rojo N-S:** {rojo_II_fase_NS:.2f} s")
            st.info(verificar_tiempo_rojo('E-O', rojo_I_fase_EO, tc))
            st.info(verificar_tiempo_rojo('N-S', rojo_II_fase_NS, tc))

        # =======================
        # AJUSTES NECESARIOS
        # =======================
        if rojo_I_fase_EO < tc or rojo_II_fase_NS < tc:
            st.warning("⚠️ Tiempo de cruce insuficiente. Ajustando parámetros...")

            (
                _, verde_fase_II_nuevo, verde_fase_I_nuevo,
                C_nuevo, verde_fase_I_real, verde_fase_II_real
            ) = ajustar_tiempos(tc, TR, tp, yp_1, yp_2, ta, T)

            R_EO_nuevo = rojo(C_nuevo, verde_fase_I_real)
            R_NS_nuevo = rojo(C_nuevo, verde_fase_II_real)

            st.subheader("🛠️ Ajustes Realizados")
            with st.expander("📐 Nuevos Parámetros Calculados"):
                st.markdown(f"- 🔁 **Nuevo ciclo:** {C_nuevo:.2f} s")
                st.markdown(f"- 🟩 **Verde real E-O:** {verde_fase_I_real:.2f} s")
                st.markdown(f"- 🟩 **Verde real N-S:** {verde_fase_II_real:.2f} s")
                st.markdown(f"- 🔴 **Rojo E-O:** {R_EO_nuevo:.2f} s")
                st.markdown(f"- 🔴 **Rojo N-S:** {R_NS_nuevo:.2f} s")

            st.subheader("🚦 Diagrama Vehicular Ajustado")
            st.pyplot(graficar_fases(C_nuevo, verde_fase_I_real, verde_fase_II_real, ta, TR))

            st.subheader("🚸 Diagrama Peatonal Ajustado")
            st.pyplot(graficar_fases_peatonal(
                verde_fase_I_real, verde_fase_II_real,
                R_EO_nuevo, R_NS_nuevo, ta, TR, C_nuevo
            ))

    except Exception as e:
        st.error(f"❌ Error en el cálculo: {str(e)}")
        st.warning("⚠️ Verifique los parámetros de entrada y vuelva a intentarlo.Interseccion Sobresaturada")

# =======================
# PIE DE PÁGINA
# =======================
st.markdown("""
<hr>
<div style='text-align: center; font-size: 0.9em; color: gray;'>
    <p>© 2025 <strong>Traffic_Light_Kevin_Galindo_Antezana</strong> | All rights reserved, please reference.</p>
    <p>📧 Contact: <a href="mailto:keds1810@gmail.com">keds1810@gmail.com</a></p>
    <p>Developed with Python + Streamlit</p>
    <p><a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a></p>
    </div>

""", unsafe_allow_html=True)
