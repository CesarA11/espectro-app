# Aplicación de Gráfico de Espectro

Esta aplicación permite visualizar señales en el espectro radioeléctrico, incluyendo el cálculo del ruido térmico en función de la temperatura y la representación gráfica de hasta tres señales con diferentes parámetros.

---

## Funcionalidades

- Cálculo del nivel de ruido térmico con base en la temperatura (K).
- Visualización simultánea de hasta 3 señales.
- Cálculo del espectro en potencia (dBm).
- Gráfico con las señales y su conexión al piso de ruido.
- Interfaz móvil opcional mediante MIT App Inventor conectada al backend.
- También ejecutable desde cualquier navegador a través de [Streamlit Cloud](https://espectro-app-et4hxc9tsyxaz8subsdb7k.streamlit.app/).

---

## ¿Cómo usarla?

1. Desde tu celular abre la aplicación App Inventor conectada.
2. Ingresa:
   - Frecuencia central
   - Ancho de banda
   - Temperatura
   - Potencia de las señales
3. Presiona el botón “Generar gráfica”.
4. El servidor devuelve la gráfica del espectro.

---

## Tecnologías utilizadas

- MIT App Inventor (Interfaz móvil)
- PythonAnywhere (Backend en Python)
- HTTP Requests
- Matplotlib (para graficar señales)

---

## Autor

**Cesar Ivan Aguilar Huerfa** – Tecnologia en Sistematizacion de Datos
Universidad Distrital Francisco Jose de Caldas – Redes Inalámbricas


