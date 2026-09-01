# Sistema de Forecasting Inteligente para Movilidad Urbana

🔗 **Prueba el Simulador Interactivo (What-If):** [Clic aquí para acceder a la aplicación](https://prediccion-demanda-buses-urbanos-aqbqzlxvicuorbaeuqzgua.streamlit.app/)[cite: 5]

## Resumen del Proyecto

Este repositorio contiene el código y los datos de un sistema predictivo diseñado para anticipar la demanda mensual de pasajeros en rutas de autobuses urbanos[cite: 5]. El modelo analiza cuatro regiones clave: Asturias, Galicia, País Vasco y Madrid[cite: 5]. 

Abandonando los promedios simples tradicionales, el sistema utiliza **Inteligencia Artificial (XGBoost)** para cruzar la inercia histórica de movilidad (datos del INE) con factores externos como la meteorología local (AEMET) y el calendario laboral[cite: 5].

## Contenido del Repositorio

En este repositorio se incluyen todos los ficheros pertinentes para la comprensión y ejecución del proyecto:
*   **Base de Datos:** Se crearon y ejecutaron pipelines de limpieza y unión de las bases de datos obtenidas del INE y del AEMET.
*   **Informe Completo (PDF):** Documento detallado que abarca el análisis exploratorio de datos, la construcción de los modelos predictivos y la explicación de uso del simulador para el negocio[cite: 5].
*   **Código y Modelos:** Scripts de análisis y entrenamiento, los archivos `.pkl` con los algoritmos XGBoost ya entrenados para cada región, y el archivo `app.py` que da vida a la interfaz.
*   **Entorno:** Archivo `requirements.txt` con las dependencias necesarias para replicar el proyecto.

## Ingeniería de Datos y Estrategia de Modelado

Para garantizar la máxima precisión en entornos de producción, se tomaron las siguientes decisiones estratégicas:

*   **Limpieza estructural:** Se eliminó por completo el periodo de pandemia (marzo 2020 - junio 2021) del conjunto de entrenamiento para evitar que el algoritmo asimilara un patrón de colapso anómalo[cite: 5].
*   **Modelado descentralizado:** Se desarrollaron modelos independientes por Comunidad Autónoma para impedir que el volumen masivo de Madrid generara un sesgo de escala que ocultara las dinámicas del norte peninsular[cite: 5].
*   **Enfoque de crecimiento:** El objetivo matemático se transformó para predecir el ritmo de crecimiento interanual en lugar de totales absolutos, permitiendo a la IA pronosticar récords históricos sin verse limitada por "techos" pasados[cite: 5].
*   **Ajuste de hiperparámetros:** Se utilizó una profundidad de árbol (max_depth) de nivel 3 en Galicia para capturar su fuerte estacionalidad, y un nivel 2 en el resto como regularizador frente al ruido climático[cite: 5].

## Resultados y Despliegue Operativo

Los modelos predictivos han demostrado una fiabilidad excepcional en el conjunto de test (2025-2026)[cite: 5]:

*   **Precisión de excelencia:** El sistema mantiene un Error Porcentual Absoluto Medio (MAPE) inferior al 6% en todas las regiones analizadas[cite: 5].
*   **Hitos por región:** Destaca la exactitud lograda en Galicia (MAPE del 2,12%) y en Asturias (MAPE del 3,66%)[cite: 5].
*   **Impacto de negocio:** El algoritmo se ha encapsulado en un Simulador Interactivo en la nube que permite a los equipos de operaciones y finanzas simular escenarios climáticos para optimizar flotas y prever flujos de caja[cite: 5].
