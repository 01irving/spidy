# energy.py
import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Gasto Energético 24h",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Función para calcular BMR según Schofield
def calcular_bmr_schofield(edad, sexo, peso):
    """Calcula la Tasa Metabólica Basal usando ecuaciones de Schofield"""
    try:
        if sexo == 'M':
            if edad < 3: return 59.512 * peso - 30.4
            elif edad < 10: return 22.706 * peso + 504.3
            elif edad < 18: return 17.686 * peso + 658.2
            elif edad < 30: return 15.057 * peso + 692.2
            elif edad < 60: return 11.472 * peso + 873.1
            else: return 11.711 * peso + 587.7
        else:
            if edad < 3: return 58.317 * peso - 31.1
            elif edad < 10: return 20.315 * peso + 485.9
            elif edad < 18: return 13.384 * peso + 692.6
            elif edad < 30: return 14.818 * peso + 486.6
            elif edad < 60: return 8.126 * peso + 845.6
            else: return 9.082 * peso + 658.5
    except Exception as e:
        st.error(f"Error en cálculo BMR: {str(e)}")
        return None

# Cargar datos de actividades
@st.cache_data
def cargar_actividades():
    try:
        datos = pd.read_csv("compendio.csv")
        return datos.rename(columns={
            'CODIGO': 'ID',
            'MET': 'METS',
            'CATEGORIA': 'CATEGORIA',
            'ACTIVIDAD ESPECIFICA': 'ACTIVIDAD'
        })
    except Exception as e:
        st.error(f"Error al cargar actividades: {str(e)}")
        st.stop()

# Interfaz principal
st.title("🔥 Calculadora de Gasto Energético 24h")
st.markdown("""
Calcula tu gasto energético diario considerando:
1. Metabolismo basal (ecuación de Schofield)
2. Actividad física específica (METs)
3. Nivel de actividad general (PAL)
""")

# Sección 1: Datos personales
with st.expander("🧍 Datos Personales", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        edad = st.number_input("Edad (años)", min_value=1, max_value=120, value=30)
    with col2:
        sexo = st.radio("Sexo", ['M', 'F'], horizontal=True)
    with col3:
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0)

# Sección 2: Actividad física
with st.expander("🏋️ Actividad Física", expanded=True):
    datos_act = cargar_actividades()
    
    col1, col2 = st.columns(2)
    with col1:
        categoria = st.selectbox("Categoría", sorted(datos_act['CATEGORIA'].unique()))
        actividades = datos_act[datos_act['CATEGORIA'] == categoria]
        actividad = st.selectbox(
            "Actividad específica",
            actividades['ACTIVIDAD'],
            format_func=lambda x: f"{x} ({actividades[actividades['ACTIVIDAD'] == x]['METS'].values[0]} METs)"
        )
    with col2:
        horas_actividad = st.slider(
            "Horas dedicadas",
            min_value=0.0,
            max_value=24.0,
            value=1.0,
            step=0.5,
            help="Horas diarias dedicadas a esta actividad"
        )

# Sección 3: Actividad general
with st.expander("🏃 Nivel de Actividad General (PAL)", expanded=True):
    st.markdown("""
    **Explicación PAL:**
    - **1.2:** Reposo en cama
    - **1.2-1.6:** Sedentario (oficina, poco ejercicio)
    - **1.6-2.0:** Activo (ejercicio regular)
    - **>2.0:** Muy activo (trabajo físico intenso)
    """)
    
    pal = st.number_input(
        "Ingrese su PAL (Nivel de Actividad Física)",
        min_value=1.2,
        max_value=2.5,
        value=1.5,
        step=0.1,
        format="%.2f",
        help="Nivel de Actividad Física General (valores como 1.45, 1.78, 2.15)"
    )

# Cálculos y resultados
if st.button("Calcular Gasto Energético"):
    try:
        # Calcular componentes
        bmr = calcular_bmr_schofield(edad, sexo, peso)
        mets = actividades[actividades['ACTIVIDAD'] == actividad]['METS'].values[0]
        
        horas_reposo = 24 - horas_actividad
        
        # Calcular componentes energéticos
        componente_reposo = (bmr * pal) * (horas_reposo / 24)
        componente_actividad = mets * peso * horas_actividad
        tee_total = componente_reposo + componente_actividad

        # Mostrar resultados
        st.divider()
        st.subheader("📊 Resultados del Cálculo")
        
        # Métricas principales
        col1, col2, col3 = st.columns(3)
        col1.metric("Metabolismo Basal (BMR)", f"{bmr:.0f} kcal")
        col2.metric("Gasto por Actividad o ejercicio", f"{componente_actividad:.0f} kcal")
        col3.metric("Gasto Total 24h (TEE)", f"{tee_total:.0f} kcal", delta_color="off")
        
        # Desglose detallado
        with st.expander("🔍 Ver desglose detallado"):
            st.markdown(f"""
            **Descomposición del cálculo:**
            - **Horas de actividad general y sueño:** {horas_reposo:.1f}h
           - **Componente de actividad general y sueño:** {bmr:.0f} × {pal} × ({horas_reposo:.1f}/24) = {componente_reposo:.0f} kcal
          - **Horas de ejercicio:** {horas_actividad:.1f}h
            - **Componente ejercicio:** {mets} METs × {peso}kg × {horas_actividad:.1f}h = {componente_actividad:.0f} kcal
            """)
            
    except Exception as e:
        st.error(f"Error en los cálculos: {str(e)}")

# Notas finales
st.divider()
st.markdown("""
**Notas importantes:**
1. Los cálculos son estimaciones basadas en ecuaciones estándar
2. Para mayor precisión, consultar con un profesional de nutrición
3. El PAL se aplica a las horas dedicadas a actividades no relacionadas al ejercicio y al sueño
4. Los valores de METs son promedios de referencia
5. Considerar variaciones individuales en el metabolismo
""")

# Para ejecutar:
# streamlit run energy.py