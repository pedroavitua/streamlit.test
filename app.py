import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables de estado que se conservan cuando Streamlit
# vuelve a ejecutar el script

if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iteraciones', 'media']
    )

# Título de la aplicación
st.header('Lanzar una moneda')

# Crear un contenedor vacío para el gráfico
chart = st.empty()

# Lista para almacenar los valores del gráfico
chart_data = [0.5]

# Mostrar el gráfico inicial
chart.line_chart(chart_data)


# Función para simular los lanzamientos de moneda
def toss_coin(n):

    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:

        outcome_no += 1

        if r == 1:
            outcome_1_count += 1

        # Calcular la media acumulada
        mean = outcome_1_count / outcome_no

        # Agregar el nuevo valor a la lista
        chart_data.append(mean)

        # Actualizar el gráfico completo
        chart.line_chart(chart_data)

        # Pausa para visualizar la evolución
        time.sleep(0.05)

    return mean


# Control deslizante
number_of_trials = st.slider(
    '¿Número de intentos?',
    1,
    1000,
    10
)

# Botón para ejecutar el experimento
start_button = st.button('Ejecutar')


if start_button:

    st.write(
        f'Experimento con {number_of_trials} intentos en curso.'
    )

    # Incrementar el número de experimento
    st.session_state['experiment_no'] += 1

    # Ejecutar la simulación
    mean = toss_coin(number_of_trials)

    # Guardar los resultados en un DataFrame
    new_result = pd.DataFrame(
        data=[[
            st.session_state['experiment_no'],
            number_of_trials,
            mean
        ]],
        columns=['no', 'iteraciones', 'media']
    )

    st.session_state['df_experiment_results'] = pd.concat(
        [
            st.session_state['df_experiment_results'],
            new_result
        ],
        ignore_index=True
    )


# Mostrar el historial de experimentos
st.write(st.session_state['df_experiment_results'])