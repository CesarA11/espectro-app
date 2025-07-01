## Aplicación de Gráfico de Espectro

Esta aplicación permite visualizar señales en el espectro radioeléctrico, incluyendo el cálculo del ruido térmico en función de la temperatura y la representación gráfica de hasta tres señales con diferentes parámetros.

---

## Funcionalidades

- Cálculo del nivel de ruido térmico según la temperatura y el ancho de banda.
- Visualización simultánea de hasta 3 señales.
- Cálculo del espectro en potencia (dBm).
- Gráfico con las señales y su conexión al piso de ruido.
- También ejecutable desde cualquier navegador a través de [Streamlit Cloud](https://espectro-app-et4hxc9tsyxaz8subsdb7k.streamlit.app/).

---

## Parámetros de Entrada

# Generales:
- Temperatura (K)
- Ancho de banda del medidor (Hz)
- Ruido adicional del sistema (dB)

# Señales:
- Frecuencia central Fc (MHz)
- Ancho de banda BW (MHz)
- Potencia (dBm)

---

## ¿Cómo usarla?

1. Accede directamente desde cualquier navegador usando el siguiente enlace:
[https://espectro-app-et4hxc9tsyxaz8subsdb7k.streamlit.app/](https://espectro-app-et4hxc9tsyxaz8subsdb7k.streamlit.app/) No requiere instalación, solo acceso a Internet..
2. El código está disponible en GitHub desde el repositorio : [https://github.com/CesarA11/espectro-app.git] (espectro-app).
3. Ingresa los valores de temperatura, ancho de banda y señales.
4. La gráfica se actualiza automáticamente con las señales dominantes por frecuencia.
5. Observa el comportamiento de cada señal respecto al ruido térmico.

---

## Tecnologías utilizadas

- [Python 3](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Matplotlib](https://matplotlib.org/)
- [NumPy](https://numpy.org/)

## Autor

Cesar Ivan Aguilar Huerfa
Redes Inalámbricas
Tecnologia en Sistematizacion de Datos
Universidad Distrital Francisco Jose de Caldas



