# Cesar Aguilar - Univesidad Distrital Francisco Jose de Caldas
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constante de Boltzmann
k = 1.38e-23  # J/K

# Título
st.title("Espectro con Señales tipo Campana (Forma de Cono)")

# Parámetros generales
st.header("Parámetros Generales")
T = st.number_input("Temperatura (K)", value=300.0)
bw_medidor = st.number_input("Ancho de banda del medidor (Hz)", value=50_000.0)
ruido_adicional = st.number_input("Ruido adicional del sistema (dB)", value=0.0)

# Ruido térmico
P_ruido_W = k * T * bw_medidor
P_ruido_W = max(P_ruido_W, 1e-20)
P_ruido_dBm = 10 * np.log10(P_ruido_W) + 30 + ruido_adicional
st.markdown(f"**Nivel de ruido térmico:** {P_ruido_dBm:.2f} dBm")

# Entradas de señales
senales = []
st.header("Parámetros de Señales")

for i in range(3):
    with st.expander(f"Señal {i+1}"):
        fc = st.number_input(f"Frecuencia central Fc{i+1} (MHz)", value=200 + i*10)
        bw = st.number_input(f"Ancho de banda BW{i+1} (MHz)", value=1.0*(2**i))  # 1, 4, 10 por defecto
        pot_dbm = st.number_input(f"Potencia{i+1} (dBm)", value=0.0)
        senales.append({"Fc": fc, "BW": bw, "P_dBm": pot_dbm})

# Gráfico
fig, ax = plt.subplots()

for señal in senales:
    fc = señal["Fc"]
    BW = señal["BW"]
    P_dBm = señal["P_dBm"]

    if BW > 0:
        f1 = fc - BW / 2
        f2 = fc + BW / 2
        f = np.linspace(f1, f2, 200)

        # Señal con forma de campana (cuadrática invertida)
        # y = -a*(f - fc)^2 + P_dBm
        a = 4 * (P_dBm - (P_ruido_dBm - 10)) / (BW**2)  # parámetro para que llegue a P_dBm en el centro
        p = -a * (f - fc)**2 + P_dBm
        p = np.maximum(p, P_ruido_dBm - 20)  # cortar para evitar valores muy bajos

        ax.plot(f, p, label=f"Fc={fc} MHz, BW={BW} MHz, Pot={P_dBm} dBm")

# Línea de ruido
ax.axhline(P_ruido_dBm, color="k", linestyle="--", label=f"Ruido térmico: {P_ruido_dBm:.2f} dBm")

# Ejes y estilo
ax.set_xlabel("Frecuencia (MHz)")
ax.set_ylabel("Potencia (dBm)")
ax.set_title("Espectro con Señales tipo Campana (Forma de Cono)")
max_p = max(s["P_dBm"] for s in senales)
ax.set_ylim(P_ruido_dBm - 10, max(max_p + 5, 10))
ax.grid(True)
ax.legend()

# Mostrar
st.pyplot(fig)
