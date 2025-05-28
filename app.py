import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constante de Boltzmann
k = 1.38e-23  # J/K

# Encabezado
st.title("Gráfico del Espectro Radioeléctrico")

# Parámetros generales
st.header("Parámetros Generales")
T = st.number_input("Temperatura (K)", value=300.0)
bw_medidor = st.number_input("Ancho de banda del medidor (Hz)", value=50_000.0)
ruido_adicional = st.number_input("Ruido adicional del sistema (dB)", value=0.0)


# Cálculo físico del ruido térmico
P_ruido_W = k * T * bw_medidor
P_ruido_W = max(P_ruido_W, 1e-20)  # evitar log(0)
P_ruido_dBm = 10 * np.log10(P_ruido_W) + 30 + ruido_adicional

# Mostrar resultado
st.markdown(f"**Nivel de ruido térmico:** {P_ruido_dBm:.2f} dBm")

# Parámetros de señales
senales = []
st.header("Parámetros de Señales")


# Formulario para cada señal
for i in range(3):
    with st.expander(f"Señal {i+1}"):
        fc = st.number_input(f"Frecuencia central Fc{i+1} (MHz)", value=200 + i * 10)
        bw = st.number_input(f"Ancho de banda BW{i+1} (MHz)", value=10.0)
        pot_dbm = st.number_input(f"Potencia{i+1} (dBm)", value=0.0)
        pot_mw = 10 ** (pot_dbm / 10)  # Conversión a mW
        senales.append({"Fc": fc, "BW": bw, "P": pot_mw, "P_dBm": pot_dbm})

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

        ax.plot(f_ext, p_ext, label=f"Fc={fc} MHz, Pot={señal['P_dBm']} dBm")

# Línea de ruido térmico
ax.axhline(P_ruido_dBm, color="k", linestyle="--", label=f"Ruido térmico: {P_ruido_dBm:.2f} dBm")

# Ejes y leyenda
ax.set_xlabel("Frecuencia (MHz)")
ax.set_ylabel("Potencia (dBm)")
ax.set_title("Espectro de Señales con Ruido Térmico")
max_p_mw = np.nanmax([s["P"] for s in senales] + [1e-12])
ax.set_ylim(P_ruido_dBm - 10, 10 * np.log10(max_p_mw) + 40)
ax.grid(True)
ax.legend()

# Mostrar gráfico
st.pyplot(fig)
