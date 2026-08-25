import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS CORPORATIVOS (CIAN ALSA)
st.set_page_config(page_title="Simulador de Demanda - Alsa", layout="wide")

# Inyección de CSS para forzar modo oscuro y usar el color #3FC8EB
st.markdown("""
    <style>
        /* Fondo oscuro y texto blanco */
        .stApp {
            background-color: #121212;
            color: #FFFFFF;
        }
        /* Color principal Cian Alsa para Títulos */
        h1, h2, h3 {
            color: #3FC8EB !important;
        }
        /* Estilo de la caja de predicción final */
        div[data-testid="metric-container"] {
            background-color: #1e1e1e;
            border: 2px solid #3FC8EB;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(63, 200, 235, 0.2);
        }
        div[data-testid="metric-container"] label {
            color: #3FC8EB !important;
            font-size: 1.2rem;
            font-weight: bold;
        }
        /* Sliders y botones color corporativo */
        .stSlider > div > div > div > div {
            background-color: #3FC8EB !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. CARGA DE DATOS Y CACHÉ
@st.cache_data
def load_data():
    df = pd.read_excel('dataset_modelo_final.xlsx')
    df['fecha'] = pd.to_datetime(df['fecha'])
    return df

df = load_data()

# Título del Dashboard
st.title("🚍 Simulador Predictivo de Demanda de Viajeros (What-If)")
st.write("Configura los escenarios climáticos y de calendario para predecir el impacto en la venta de billetes.")
st.markdown("---")

# 3. BARRA LATERAL (MENÚ DE CONTROLES)
st.sidebar.header("⚙️ Parámetros del Escenario")

# Selección de Región
region_seleccionada = st.sidebar.selectbox(
    "Selecciona la Comunidad Autónoma:",
    ['Asturias', 'Galicia', 'País Vasco', 'Madrid']
)

# Selección del Mes Base (Para calcular los Lags automáticamente)
# Tomamos los últimos meses disponibles en tu histórico para usar como base real
fechas_disponibles = df['fecha'].dt.strftime('%Y-%m').sort_values().unique()[-24:] 
mes_base = st.sidebar.selectbox(
    "Mes de Referencia (Para extraer inercia histórica):",
    fechas_disponibles,
    index=len(fechas_disponibles)-1
)

st.sidebar.markdown("---")
st.sidebar.subheader("🌤️ Escenario Meteorológico")
np_010 = st.sidebar.slider("Días con Lluvia al mes:", 0, 31, 10)
nt_30 = st.sidebar.slider("Días con Calor Extremo (>30º):", 0, 31, 5)
n_des = st.sidebar.slider("Días Totalmente Despejados:", 0, 31, 12)

st.sidebar.markdown("---")
st.sidebar.subheader("📅 Escenario de Calendario")
dias_libres = st.sidebar.slider("Días Libres Totales (Fines de semana + Festivos):", 8, 14, 10)
semana_santa = st.sidebar.selectbox("¿Incluye Semana Santa?", [0, 1])

# 4. PROCESAMIENTO Y MOTOR PREDICTIVO
# Extraemos el mes exacto del dataset para ver cuántos viajeros hubo realmente (Lags)
df_filtro = df[(df[region_seleccionada] == 1) & (df['fecha'].dt.strftime('%Y-%m') == mes_base)]

if df_filtro.empty:
    st.error("No hay datos históricos para calcular la inercia de este mes.")
else:
    # Extracción de la inercia (El modelo necesita saber qué pasó el mes y el año anterior)
    viajeros_lag1 = df_filtro['VIAJEROS_lag1'].values[0]
    viajeros_lag12 = df_filtro['VIAJEROS_lag12'].values[0]
    mes_num = df_filtro['mes'].values[0]
    
    ratio_lag1 = viajeros_lag1 / (viajeros_lag12 + 1e-5)
    
    # Construcción del vector que enviaremos a la Inteligencia Artificial
    X_simulado = pd.DataFrame({
        'np_010': [np_010],
        'nt_30': [nt_30],
        'n_des': [n_des],
        'mes': [mes_num],
        'dias_libres_totales': [dias_libres],
        'semana_santa': [semana_santa],
        'RATIO_LAG1': [ratio_lag1]
    })
    
    # Carga del modelo específico .pkl
    nombre_modelo = f'modelo_XGB_{region_seleccionada.replace(" ", "_")}.pkl'
    try:
        modelo_xgb = joblib.load(nombre_modelo)
        
        # Predicción matemática
        pred_delta = modelo_xgb.predict(X_simulado)[0]
        pred_final_absoluta = viajeros_lag12 + pred_delta
        
        # 5. PANEL DE RESULTADOS VISUALES
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📊 Predicción de Demanda")
            st.metric(
                label=f"Viajeros Estimados ({region_seleccionada})", 
                value=f"{int(pred_final_absoluta):,} u.",
                delta=f"{int(pred_delta):,} respecto al año pasado"
            )
            
        with col2:
            st.subheader("🔍 Desglose del Escenario Matemático")
            st.write(f"Para calcular este volumen, el sistema ha partido de una base inercial de **{int(viajeros_lag12):,} viajeros** del año anterior.")
            st.write("Al aplicar las condiciones introducidas:")
            st.markdown(f"""
            * 🌧️ Lluvia: **{np_010} días**
            * 🌡️ Calor Extremo: **{nt_30} días**
            * 🏖️ Días Libres: **{dias_libres} días**
            """)
            if pred_delta > 0:
                st.success("La Inteligencia Artificial determina que estas condiciones generan un escenario **FAVORABLE** de crecimiento.")
            else:
                st.warning("La Inteligencia Artificial determina que estas condiciones generarán una **CONTRACCIÓN** de la demanda.")
                
    except FileNotFoundError:
        st.error(f"No se encuentra el archivo {nombre_modelo}. Asegúrate de ejecutar primero tu script de exportación.")