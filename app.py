# Cesar Aguilar - Universidad Distrital Francisco Jose de Caldas
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Configurar estilo del grafico
plt.style.use('ggplot')
plt.rcParams['axes.facecolor'] = '#F5F5DC'
plt.rcParams['grid.color'] = 'black'
plt.rcParams['grid.linewidth'] = 0.8
plt.rcParams['grid.alpha'] = 0.5

# Constante de Boltzmann
k = 1.38e-23  # J/K

# Funciones
def calcular_ruido_termico(T, bw_medidor, ruido_adicional):
    P_ruido_W = k * T * bw_medidor
    P_ruido_W = max(P_ruido_W, 1e-20)
    return 10 * np.log10(P_ruido_W) + 30 + ruido_adicional

def generar_senal(fc, bw, pot_dbm, P_ruido_dBm):
    f1 = fc - bw / 2
    f2 = fc + bw / 2
    f = np.linspace(f1, f2, 500)
    a = 4 * (pot_dbm - (P_ruido_dBm - 10)) / (bw**2)
    p = -a * (f - fc)**2 + pot_dbm
    p = np.maximum(p, P_ruido_dBm - 20)
    return f, p

# Interfaz
st.markdown("## Gráfico de Espectro de Señales")
st.markdown("Cesar Aguilar - 20181578017")

# Parámetros Generales
col1, col2 = st.columns([2, 3])
with col1:
    st.header("Parámetros Generales")
    T = st.number_input("Temperatura (K)", value=300.0, min_value=1.0)
    bw_medidor = st.number_input("Ancho de banda del medidor (Hz)", value=50_000.0, min_value=1.0)
    ruido_adicional = st.number_input("Ruido adicional del sistema (dB)", value=0.0)

P_ruido_dBm = calcular_ruido_termico(T, bw_medidor, ruido_adicional)
st.markdown(f"**Ruido térmico:** `{P_ruido_dBm:.2f} dBm`")

# Señales
with col2:
    st.header("Parámetros de Señales")
    senales = []
    for i in range(3):
        with st.expander(f"Señal {i+1}"):
            fc = st.number_input(f"Frecuencia central Fc{i+1} (MHz)", value=200 + i*10)
            bw = st.number_input(f"Ancho de banda BW{i+1} (MHz)", value=20.0, min_value=0.1)
            pot_dbm = st.number_input(f"Potencia{i+1} (dBm)", value=[10.0, 15.0, 10.0][i])
            senales.append({"Fc": fc, "BW": bw, "P_dBm": pot_dbm})

# Gráfico
fig, ax = plt.subplots(figsize=(14, 8))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# Configurar fondo beige y cuadrícula
ax.set_facecolor('#F5F5DC')
ax.grid(True, color='black', linestyle='-', linewidth=0.8, alpha=0.5)

# Generar todas las señales primero
señales_generadas = []
for i, señal in enumerate(senales):
    fc, bw, p_dbm = señal["Fc"], señal["BW"], señal["P_dBm"]
    if bw <= 0:
        continue
    f, p = generar_senal(fc, bw, p_dbm, P_ruido_dBm)
    señales_generadas.append((f, p, colors[i], f"Fc={fc} MHz, BW={bw} MHz, Pot={p_dbm} dBm", fc, p_dbm))

# Combinar todas las frecuencias y encontrar el máximo en cada punto
if señales_generadas:
    all_freqs = np.unique(np.concatenate([s[0] for s in señales_generadas]))
    all_freqs.sort()
    
    # Interpolar cada señal en todas las frecuencias
    interp_señales = []
    for f, p, color, label, fc, p_dbm in señales_generadas:
        interp_p = np.interp(all_freqs, f, p)
        interp_señales.append((all_freqs, interp_p, color, label, fc, p_dbm))
    
    # Encontrar la señal dominante en cada punto
    potencia_total = np.vstack([s[1] for s in interp_señales])
    señal_dominante = np.argmax(potencia_total, axis=0)
    
    # Dibujar segmentos de cada señal donde es dominante
    for i, (f, p, color, label, fc, p_dbm) in enumerate(interp_señales):
        mask = señal_dominante == i
        segments = []
        prev_mask = False
        start_idx = 0
        
        # Crear segmentos continuos donde esta señal es dominante
        for idx, current_mask in enumerate(mask):
            if current_mask and not prev_mask:
                start_idx = idx
            elif not current_mask and prev_mask:
                segments.append((start_idx, idx-1))
            prev_mask = current_mask
        
        if prev_mask:
            segments.append((start_idx, len(mask)-1))
        
        # Dibujar cada segmento
        for start, end in segments:
            ax.plot(f[start:end+1], p[start:end+1], color=color, linewidth=3.0)
        
        # Dibujar línea segmentada más gruesa desde la frecuencia central
        ax.plot([fc, fc], [P_ruido_dBm-20, p_dbm], color=color, 
                linestyle=':', linewidth=2.5, alpha=0.8, dashes=(5, 3))
        
        # Dibujar un punto al final para que aparezca en la leyenda
        ax.plot([], [], color=color, label=label, linewidth=3.0)

# Línea de ruido
ax.axhline(P_ruido_dBm, color="red", linestyle="--", linewidth=2.0, label=f"Ruido térmico: {P_ruido_dBm:.2f} dBm")

# Estilo y etiquetas
ax.set_xlabel("Frecuencia (MHz)", fontweight='bold', fontsize=12)
ax.set_ylabel("Potencia (dBm)", fontweight='bold', fontsize=12)
ax.set_title("Gráfico de Espectro de Señales", fontweight='bold', pad=20, fontsize=14)

# Límites y marcas
if señales_generadas:
    min_f = min(s[0].min() for s in señales_generadas)
    max_f = max(s[0].max() for s in señales_generadas)
    max_p = max(s[1].max() for s in señales_generadas)
    ax.set_xlim(min_f - 10, max_f + 10)
    ax.set_ylim(P_ruido_dBm - 20, max(max_p + 10, 10))
    
    # Marcas en los ejes
    ax.set_yticks(np.arange(-140, 21, 20))
    ax.set_xticks(np.arange(190, 231, 10))

    # Resaltar marcas principales
    ax.tick_params(axis='both', which='major', labelsize=11, width=1.5)

# Mostrar
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', framealpha=1, 
          edgecolor='black', fontsize=10)
plt.tight_layout()
st.pyplot(fig)