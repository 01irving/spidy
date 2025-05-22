import streamlit as st

def calcular_tasa_sudoracion(pi_kg, pf_kg, cl_ml, orina_ml, tiempo_min):
    pi_g = pi_kg * 1000
    pf_g = pf_kg * 1000
    diferencia_peso = pi_g - pf_g
    sudor_total_ml = diferencia_peso + cl_ml - orina_ml
    if sudor_total_ml < 0:
        return None, diferencia_peso, sudor_total_ml, None, None
    tasa_sudoracion = (sudor_total_ml / tiempo_min) * 60
    perdida_peso_pct = ((pi_kg - pf_kg) / pi_kg) * 100
    return tasa_sudoracion, diferencia_peso, sudor_total_ml, perdida_peso_pct, tasa_sudoracion / 1000

# Interfaz
st.title("💧 Calculadora de Tasa de Sudoración")
st.markdown("Calcula la tasa de sudoración (ml/h) a partir de tus datos de entrenamiento.")

# Entradas del usuario
pi_kg = st.number_input("Peso inicial (kg)", min_value=0.0, format="%.2f")
pf_kg = st.number_input("Peso final (kg)", min_value=0.0, format="%.2f")
cl_ml = st.number_input("Consumo de líquidos durante el ejercicio (ml)", min_value=0.0, format="%.1f")
orina_ml = st.number_input("Pérdidas por orina (ml)", min_value=0.0, format="%.1f")
tiempo_min = st.number_input("Duración del ejercicio (min)", min_value=1.0, format="%.1f")

if st.button("Calcular tasa de sudoración"):
    ts, diferencia_peso, sudor_total, perdida_pct, ts_litros = calcular_tasa_sudoracion(
        pi_kg, pf_kg, cl_ml, orina_ml, tiempo_min
    )
    if ts is None:
        st.error("❌ Los datos ingresados generan una tasa de sudoración negativa. Verifica los valores.")
    else:
        st.success("✅ Cálculo completado con éxito.")
        st.markdown(f"**Diferencia de peso:** {diferencia_peso:.1f} g")
        st.markdown(f"**Pérdida total de sudor:** {sudor_total:.1f} ml")
        st.markdown(f"**Tasa de sudoración:** {ts:.2f} ml/h ({ts_litros:.2f} L/h)")
        st.markdown(f"**Pérdida de peso corporal:** {perdida_pct:.2f}%")
        if perdida_pct <= 2:
            st.info("Hidratación adecuada (pérdida ≤ 2%).")
        else:
            st.warning("¡Atención! Exceso de pérdida de peso corporal (> 2%). Ajustar hidratación.")

st.markdown("---")
st.caption("Desarrollado con ❤️ en Streamlit | Basado en datos del GSSI y ACSM")
