import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Gráfico del Espectro Radioeléctrico")

# Entradas para el usuario
temperatura = st.number_input("Temperatura (K)", min_value=0.0, value=290.0)
senales = []

# Formulario para cada señal
for i in range(3):
    with st.expander(f"Señal {i+1}"):
        fc = st.number_input(f"Frecuencia central Fc{i+1} (MHz)", value=200 + i * 10)
        bw = st.number_input(f"Ancho de banda BW{i+1} (MHz)", value=10.0)
        pot = st.number_input(f"Potencia{i+1} (mW)", value=1.0)
        senales.append({"Fc": fc, "BW": bw, "P": pot})

# Constante de Boltzmann
k = 1.38e-23  # J/K

# Cálculo del ruido térmico para el mayor BW ingresado
BW_max_Hz = max([s["BW"] for s in senales]) * 1e6  # Convertir de MHz a Hz
P_ruido = k * temperatura * BW_max_Hz  # W
P_ruido = max(P_ruido, 1e-20)  # evitar log(0)
P_ruido_dBm = 10 * np.log10(P_ruido) + 30  # convertir a dBm

# Gráfico
fig, ax = plt.subplots()

for i, señal in enumerate(senales):
    fc = señal["Fc"]
    BW = señal["BW"]
    P = señal["P"]

    if BW > 0 and P > 0:
        f = np.linspace(fc - BW / 2, fc + BW / 2, 500)
        p_gauss = P * np.exp(-((f - fc) ** 2) / (2 * (BW / 2.355) ** 2))
        p_gauss = np.maximum(p_gauss, 1e-12)
        p_gauss_dbm = 10 * np.log10(p_gauss) + 30

        # Extiende el gráfico para "conectar" al piso de ruido
        f_ext = np.concatenate([[f[0] - 2], f, [f[-1] + 2]])
        p_ext = np.concatenate([[10 * np.log10(1e-12) + 30], p_gauss_dbm, [10 * np.log10(1e-12) + 30]])

        ax.plot(f_ext, p_ext, label=f"Fc={fc} MHz")

# Línea de ruido térmico
ax.axhline(P_ruido_dBm, color="k", linestyle="--", label=f"Ruido térmico: {P_ruido_dBm:.2f} dBm")

# Ejes y leyenda
ax.set_xlabel("Frecuencia (MHz)")
ax.set_ylabel("Potencia (dBm)")
ax.set_title("Espectro de Señales con Ruido Térmico")
max_p = np.nanmax([s["P"] for s in senales] + [1])
ax.set_ylim(P_ruido_dBm - 10, 10 * np.log10(max_p) + 40)
ax.grid(True)
ax.legend()

# Mostrar gráfico
st.pyplot(fig)
