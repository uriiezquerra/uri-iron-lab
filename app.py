import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="URI IRON LAB", page_icon="🚫", layout="wide")

# Estilo visual agresivo
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; font-weight: bold; }
    .stMetric { background-color: #1a1c23; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# Sistema de Rangos (Solo para los que sufren)
def calcular_rango(puntos):
    if puntos < 2000: return "💀 CARNE DE CAÑÓN (Débil)"
    if puntos < 5000: return "⚔️ GUERRERO (Aceptable)"
    if puntos < 8500: return "🎖️ VETERANO (Respetable)"
    if puntos < 12000: return "💎 ELITE (Bestia)"
    return "👑 LEYENDA (Inalcanzable)"

# --- BASE DE DATOS E HISTORIAL ---
if 'historial' not in st.session_state:
    st.session_state.historial = pd.DataFrame(columns=['Fecha', 'Ejercicio', 'Peso', 'Reps', 'Puntos', 'Estado'])

st.title("🚫 URI: NO EXCUSES LAB")
st.write("---")

# --- PANEL DE CONTROL CRÍTICO ---
col_menu, col_stats = st.columns([1, 2])

with col_menu:
    st.header("🕵️ Juez de Sobrecarga")
    ejercicio = st.selectbox("Ejercicio a evaluar:", ["Prensa", "V-Squat", "Press Inclinado", "Hip Thrust", "Extensiones"])
    
    # Récord anterior (Simulación estricta)
    st.markdown("### 📊 Último Récord")
    peso_ant = st.number_input("Peso anterior (kg)", value=130.0)
    reps_ant = st.number_input("Reps anteriores", value=12)
    
    st.write("---")
    st.header("⚖️ Batalla de Hoy")
    peso_hoy = st.number_input("Peso Hoy (kg)", step=2.5)
    reps_hoy = st.number_input("Reps Hoy", step=1)
    fallo_real = st.toggle("¿FALLO REAL? (Si mientes, te mientes a ti mismo)")

with col_stats:
    st.header("📈 Veredicto del Coach")
    
    # LÓGICA FIRME DE SOBRECARGA
    if reps_hoy > 0:
        puntos = (peso_hoy * reps_hoy) * (1.2 if fallo_real else 1.0)
        
        if peso_hoy > peso_ant or (peso_hoy == peso_ant and reps_hoy > reps_ant):
            st.success(f"### PROGRESO DETECTADO: +{puntos:.0f} pts")
            st.write("Has cumplido. Has puesto un ladrillo más. Pero mañana esto será tu nuevo mínimo.")
            estado = "✅ PROGRESO"
        elif peso_hoy == peso_ant and reps_hoy == reps_ant:
            st.warning("### ESTANCAMIENTO: 0 pts de mejora")
            st.write("Has repetido lo que ya sabías hacer. Eso no es entrenar, es mantener el sitio. Exígete más en la siguiente serie.")
            estado = "⚠️ ESTANCADO"
        else:
            st.error("### RETROCESO: Rendimiento mediocre")
            st.write("Menos peso o menos reps que la última vez. O no has comido, o no has dormido, o te ha faltado voluntad. Rectifica ya.")
            estado = "❌ FRACASO"

        # Guardar resultado
        if st.button("REGISTRAR Y CERRAR BOCA"):
            nueva_data = pd.DataFrame([[datetime.date.today(), ejercicio, peso_hoy, reps_hoy, puntos, estado]], 
                                     columns=['Fecha', 'Ejercicio', 'Peso', 'Reps', 'Puntos', 'Estado'])
            st.session_state.historial = pd.concat([st.session_state.historial, nueva_data], ignore_index=True)
            st.rerun()

# --- RANKED Y GRÁFICAS ---
st.write("---")
st.header("🏆 Clasificación de Poder")
if not st.session_state.historial.empty:
    puntos_totales = st.session_state.historial['Puntos'].sum()
    rango = calcular_rango(puntos_totales)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("VOLUMEN TOTAL", f"{puntos_totales:.0f} kg")
    c2.metric("RANGO", rango)
    c3.metric("ESTADO ACTUAL", "MUTANDO" if puntos_totales > 5000 else "CALENTANDO")

    st.subheader("📜 Diario de Guerra")
    st.dataframe(st.session_state.historial.sort_values(by='Fecha', ascending=False), use_container_width=True)
else:
    st.info("El historial está vacío. El hierro te está esperando.")
