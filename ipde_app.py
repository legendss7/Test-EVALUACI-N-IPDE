import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Definir preguntas y las opciones de respuestas (Verdadero, Falso)
questions = [
    "Normalmente me divierto y disfruto de la vida",
    "Confío en la gente que conozco",
    "No soy minucioso con los detalles pequeños",
    "No puedo decidir qué tipo de persona quiero ser",
    "Muestro mis sentimientos a todo el mundo",
    "Dejo que los demás tomen decisiones importantes por mí",
    "Me preocupo si oigo malas noticias sobre alguien que conozco",
    "Ceder a algunos de mis impulsos me causa problemas",
    "Mucha gente que conozco me envidia",
    "Doy mi opinión general sobre las cosas y no me preocupo por los detalles",
    "Nunca me han detenido",
    "La gente cree que soy frío y distante",
    "Me meto en relaciones muy intensas pero poco duraderas",
    "La mayoría de la gente es justa y honesta conmigo",
    "La gente tiene una gran opinión sobre mí",
    "Me siento molesto o fuera de lugar en situaciones sociales",
    "Me siento fácilmente influido por lo que me rodea",
    "Normalmente me siento mal cuando hago daño o molesto a alguien",
    "Me resulta muy difícil tirar las cosas",
    "A veces he rechazado un trabajo, incluso aunque estuviera esperándolo",
    "Cuando me alaban o critican manifiesto mi reacción a los demás",
    "Uso a la gente para lograr lo que quiero",
    "Paso demasiado tiempo tratando de hacer las cosas perfectamente",
    "A menudo, la gente se ríe de mí, a mis espaldas",
    "Nunca he amenazado con suicidarme, ni me he autolesionado a propósito",
    "Mis sentimientos son como el tiempo, siempre están cambiando",
    "Para evitar críticas prefiero trabajar solo",
    "Me gusta vestirme para destacar entre la gente",
    "Mentiría o haría trampas para lograr mis propósitos",
    "Soy más supersticioso que la mayoría de la gente",
    "Tengo poco o ningún deseo de mantener relaciones sexuales",
    "La gente cree que soy demasiado estricto con las reglas y normas",
    "Generalmente me siento incómodo o desvalido si estoy solo",
    "No me gusta relacionarme con gente hasta que no estoy seguro de que les gusto",
    "No me gusta ser el centro de atención",
    "Creo que mi cónyuge (amante) me puede ser infiel",
    "La gente piensa que tengo muy alto concepto de mí mismo",
    "Cuido mucho lo que les digo a los demás sobre mí",
    "Me preocupa mucho no gustar a la gente",
    "A menudo me siento vacío por dentro",
    "Trabajo tanto que no tengo tiempo para nada más",
    "Me da miedo que me dejen solo y tener que cuidar de mí mismo",
    "Tengo ataques de ira o enfado",
    "Tengo fama de que me gusta “flirtear",
    "Me siento muy unido a gente que acabo de conocer",
    "Prefiero las actividades que pueda hacer por mí mismo",
    "Pierdo los estribos y me meto en peleas",
    "La gente piensa que soy tacaño con mi dinero",
    "Con frecuencia busco consejos o recomendaciones sobre decisiones de la vida cotidiana",
    "Para caer bien a la gente me ofrezco a realizar tareas desagradables",
    "Tengo miedo a ponerme en ridículo ante gente conocida",
    "A menudo confundo objetos o sombras con gente",
    "Soy muy emocional y caprichoso",
    "Me resulta difícil acostumbrarme a hacer cosas nuevas",
    "Sueño con ser famoso",
    "Me arriesgo y hago cosas temerarias",
    "Todo el mundo necesita uno ó dos amigos para ser feliz",
    "Descubro amenazas ocultas en lo que me dicen algunas personas",
    "Normalmente trato de que la gente haga las cosas a mi manera",
    "Cuando estoy estresado las cosas que me rodean no me parecen reales",
    "Me enfado cuando la gente no quiere hacer lo que le pido",
    "Cuando finaliza una relación, tengo que empezar otra rápidamente",
    "Evito las actividades que no me resulten familiares para no sentirme molesto tratando de hacerlas",
    "A la gente le resulta difícil saber claramente que estoy diciendo.",
    "Prefiero asociarme con gente de talento",
    "He sido víctima de ataques injustos sobre mi carácter o mi reputación",
    "No suelo mostrar emoción",
    "Hago cosas para que la gente me admire",
    "Suelo ser capaz de iniciar mis propios proyectos",
    "La gente piensa que soy extraño o excéntrico",
    "Me siento cómodo en situaciones sociales",
    "Mantengo rencores contra la gente durante años",
    "Me resulta difícil no estar de acuerdo con las personas de las que dependo",
    "Me resulta difícil no meterme en líos",
    "Llego al extremo para evitar que la gente me deje",
    "Cuando conozco a alguien no hablo mucho",
    "Tengo amigos íntimos"
]

# Módulos de trastornos
disorders = {
    "Paranoide": [2, 14, 36, 38, 58, 66, 72],
    "Esquizoide": [1, 12, 21, 31, 46, 57, 77],
    "Esquizotípico": [2, 24, 30, 52, 64, 67, 70, 71],
    "Histriónico": [5, 10, 17, 26, 28, 35, 44, 45],
    "Antisocial": [11, 18, 20, 29, 47, 56, 74],
    "Narcisista": [7, 9, 15, 22, 37, 55, 61, 65, 68],
    "Límite": [4, 8, 13, 25, 40, 43, 53, 60, 75],
    "Obsesivo-Compulsivo": [19, 23, 32, 41, 48, 54, 59],
    "Dependencia": [6, 33, 42, 49, 50, 62, 69, 73],
    "Evitación": [16, 27, 34, 38, 39, 51, 63, 76]
}

# Función para almacenar respuestas
if "responses" not in st.session_state:
    st.session_state.responses = [None] * len(questions)
    st.session_state.current_question = 0

# Función para mostrar una pregunta y avanzar
def display_question():
    question_index = st.session_state.current_question
    if question_index < len(questions):
        question = questions[question_index]
        response = st.radio(question, ('Verdadero', 'Falso'), key=f"q{question_index}")
        if st.button("Siguiente"):
            st.session_state.responses[question_index] = response
            st.session_state.current_question += 1
    else:
        show_results()

# Función para mostrar los resultados
def show_results():
    st.subheader("Resultados del Cuestionario")
    results = {}
    for disorder, questions_list in disorders.items():
        true_answers = sum([1 for i in questions_list if st.session_state.responses[i - 1] == 'Verdadero'])
        if true_answers >= 3:
            results[disorder] = f"Positivo (Respuestas Verdaderas: {true_answers})"
        else:
            results[disorder] = "Negativo"

    # Mostrar los resultados con gráficos
    st.write(results)
    show_graph(results)
    generate_pdf(results)

# Función para mostrar gráficos de los resultados
def show_graph(results):
    labels = list(results.keys())
    values = [1 if result == "Positivo" else 0 for result in results.values()]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['green' if v == 1 else 'red' for v in values])
    ax.set_xlabel('Trastornos')
    ax.set_ylabel('Resultados')
    ax.set_title('Resultados del Cuestionario IPDE')
    plt.xticks(rotation=90)
    st.pyplot(fig)

# Función para generar un PDF de los resultados
def generate_pdf(results):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(72, 750, "Resumen Ejecutivo - Resultados del Cuestionario IPDE")
    y_position = 720
    for disorder, result in results.items():
        c.drawString(72, y_position, f"{disorder}: {result}")
        y_position -= 20

    c.save()
    buffer.seek(0)

    st.download_button(
        label="Descargar Informe en PDF",
        data=buffer,
        file_name="Informe_Resultados_IPDE.pdf",
        mime="application/pdf"
    )

# Interfaz del cuestionario
st.title("Test profesional creado por Leben Spa")
st.markdown("<h3 style='text-align: center;'>Cuestionario de Evaluación IPDE DSM-IV</h3>", unsafe_allow_html=True)

# Mostrar la pregunta actual
display_question()
