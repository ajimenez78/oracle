"""Content of each slide. One function per slide: (prs, number) -> None."""

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches

from deck_kit import (CYAN, LOGO_FULL, MARGIN, MUTED, NAVY, PURPLE, SLIDE_H,
                      SLIDE_W, TITLE_FONT, WHITE, accent_bar, callout, card,
                      content_slide, fill_background, number_badge, text)

CONTENT_W = SLIDE_W - 2 * MARGIN


def title_slide(prs, number):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill_background(slide, NAVY)
    slide.shapes.add_picture(str(LOGO_FULL), Inches(SLIDE_W - SLIDE_H), 0,
                             Inches(SLIDE_H), Inches(SLIDE_H))
    text(slide, 0.9, 1.9, 7, 1.2, "Oracle", size=66, color=WHITE, bold=True,
         font=TITLE_FONT)
    accent_bar(slide, 0.95, 3.15, 2.2, 0.08)
    text(slide, 0.9, 3.45, 6.6, 1.2, "Aprendizajes de la fase de Product Feedback",
         size=26, color=WHITE, font=TITLE_FONT)
    text(slide, 0.9, 4.6, 6.6, 1,
         "Un problema real de usuarios concretos, antes de empezar a construir",
         size=17, color=CYAN)
    text(slide, 0.9, 6.3, 6.6, 0.4, "Arturo, Imanol y Roberto  ·  11 de noviembre de 2026",
         size=13, color=WHITE)


def starting_point(prs, number):
    slide = content_slide(prs, "De dónde venimos", number)
    col_w = 5.5
    card(slide, MARGIN, 1.75, col_w, 3.2, "La idea inicial", [
        "Un chatbot para consultar un Second Brain en Notion.",
        "Prueba de concepto con RAG y un despliegue serverless mínimo en AWS.",
        "Foco en la etapa Express: usar las notas para crear resultados.",
    ], accent=PURPLE, heading_size=22, body_size=18)
    text(slide, MARGIN + col_w, 2.9, CONTENT_W - 2 * col_w, 0.9, "→", size=48,
         color=CYAN, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    card(slide, SLIDE_W - MARGIN - col_w, 1.75, col_w, 3.2, "El cambio de enfoque", [
        "De un proyecto técnico a un proyecto de producto.",
        "Primero, hablar con usuarios y analizar alternativas.",
        "Después, decidir qué construir.",
    ], heading_size=22, body_size=18)
    callout(slide, MARGIN, 5.45, CONTENT_W, 1.1,
            "Todo lo construido es punto de partida, no una restricción para el MVP.")


def target_user(prs, number):
    slide = content_slide(prs, "Usuario objetivo", number)
    text(slide, MARGIN, 1.6, CONTENT_W, 1.1, [[
        ("Personas que usan un ", False), ("Second Brain", True),
        (" o toman notas de forma sistemática y tienen dificultades para:", False),
    ]], size=22)
    items = [
        ("Organizar", "la información que van guardando."),
        ("Mantener", "esa organización al día."),
        ("Recuperar", "lo guardado cuando hacen un trabajo importante."),
    ]
    col_w = (CONTENT_W - 0.6) / 3
    for i, (heading, body) in enumerate(items):
        x = MARGIN + i * (col_w + 0.3)
        card(slide, x, 2.9, col_w, 2.0, heading, body,
             accent=PURPLE if i % 2 else CYAN, heading_size=24, body_size=18)
    callout(slide, MARGIN, 5.35, CONTENT_W, 1.2,
            "Quien ya tiene un método que le funciona no es nuestro usuario, "
            "pero nos enseña qué evitar: otro sistema que mantener.")


def research(prs, number):
    slide = content_slide(prs, "Cómo investigamos", number)
    stats = [
        ("2", "hilos en r/secondbrain", "uno propio y otro sobre la etapa Express"),
        ("3", "conversaciones de seguimiento", "con usuarios de la comunidad"),
        ("2", "usuarias intensivas de Notion", "profesoras, contactadas por Roberto"),
        ("15+", "alternativas analizadas", "de Notion AI a plantillas PARA"),
    ]
    col_w = (CONTENT_W - 0.9) / 4
    for i, (value, label, detail) in enumerate(stats):
        x = MARGIN + i * (col_w + 0.3)
        color = PURPLE if i % 2 else CYAN
        text(slide, x, 1.65, col_w, 1.1, value, size=60, bold=True, color=color,
             font=TITLE_FONT)
        text(slide, x, 2.85, col_w, 0.8, label, size=19, bold=True,
             font=TITLE_FONT)
        text(slide, x, 3.65, col_w, 0.8, detail, size=15, color=MUTED)
    callout(slide, MARGIN, 4.85, CONTENT_W, 1.7, [
        [("Método CODE de Tiago Forte: ", True),
         ("Capturar · Organizar · Destilar · Expresar.", False)],
        "Buscamos dónde se atascan los usuarios, separando lo que nos contaron "
        "de nuestra interpretación.",
    ])


def user_voices(prs, number):
    slide = content_slide(prs, "Qué nos contaron", number)
    voices = [
        ("e3e6", "A veces no escribe nada porque no sabe dónde ponerlo, y otras "
         "no encuentra lo que apuntó.", "El problema sin resolver más claro.", CYAN),
        ("mrz999", "Vacía dos bandejas de entrada cada día y guarda sus "
         "conclusiones en notas permanentes.",
         "Lo resuelve con una rutina personal y exigente.", PURPLE),
        ("vogelke", "Archivos simples y búsqueda rápida. Abandonó sistemas "
         "demasiado complejos.", "Lección: no añadir otro sistema que mantener.",
         PURPLE),
        ("Dos profesoras (Notion)", "Les gustaría clasificar por temática y que "
         "la herramienta pregunte cuando dude.",
         "Feedback sobre tareas. Disponibles como beta testers.", CYAN),
    ]
    col_w = (CONTENT_W - 0.3) / 2
    for i, (who, said, takeaway, color) in enumerate(voices):
        x = MARGIN + (i % 2) * (col_w + 0.3)
        y = 1.6 + (i // 2) * 2.55
        card(slide, x, y, col_w, 2.3, who, [said, [(takeaway, True)]],
             accent=color, heading_size=20, body_size=16)


def learnings(prs, number):
    slide = content_slide(prs, "Qué aprendimos", number)
    items = [
        ("La señal más clara está en organizar y recuperar",
         "Antes que en usar las notas para crear resultados (Express)."),
        ("La simplicidad es un criterio de producto",
         "Quien tiene un método que le funciona no quiere otro sistema."),
        ("Express sigue siendo prometedora",
         "La dejamos para una fase posterior, como asistente de trabajo."),
        ("La tecnología sola no nos diferencia",
         "RAG y búsqueda ya existen: el valor está en la experiencia."),
    ]
    for i, (heading, body) in enumerate(items):
        y = 1.6 + i * 1.22
        number_badge(slide, MARGIN, y + 0.15, str(i + 1),
                     color=PURPLE if i % 2 else CYAN, size=0.7)
        text(slide, MARGIN + 1.0, y, CONTENT_W - 1.0, 0.5, heading, size=22,
             bold=True, font=TITLE_FONT)
        text(slide, MARGIN + 1.0, y + 0.52, CONTENT_W - 1.0, 0.5, body, size=17,
             color=MUTED)


def competitors(prs, number):
    slide = content_slide(prs, "Competidores y alternativas", number)
    text(slide, MARGIN, 1.5, CONTENT_W, 0.6, [[
        ("El mayor competidor es la propia ", False), ("Notion", True),
        (", seguida de ", False), ("Claude o ChatGPT", True),
        (" conectados a Notion.", False),
    ]], size=20)
    rivals = [
        ("Notion AI", "Hay que saber pedírselo. Free y Plus solo tienen una prueba."),
        ("Claude / ChatGPT + MCP", "Hay que conectarlo, escribir instrucciones y vigilar los cambios."),
        ("Mem", "Organiza, pero dentro de su propia aplicación."),
        ("Obsidian", "Buenas ideas, pero fuera de Notion."),
        ("Plantillas PARA", "Una estructura vacía: no ordenan lo que ya existe."),
        ("Zapier, n8n, Make", "Clasifican lo nuevo, no el histórico."),
    ]
    col_w = (CONTENT_W - 0.6) / 3
    for i, (name, gap) in enumerate(rivals):
        x = MARGIN + (i % 3) * (col_w + 0.3)
        y = 2.45 + (i // 3) * 1.6
        card(slide, x, y, col_w, 1.45, name, gap,
             accent=PURPLE if i % 2 else CYAN, heading_size=18, body_size=15)
    callout(slide, MARGIN, 5.7, CONTENT_W, 1.0,
            "Clasificar, preguntar o deshacer existen por separado. La combinación "
            "completa no la vimos en ninguna herramienta revisada.")


def proposal(prs, number):
    slide = content_slide(prs, "Nuestra propuesta", number)
    text(slide, MARGIN, 1.55, CONTENT_W, 1.3, [[
        ("Oracle ordena el Notion que ya tienes", True),
        (", sin que tengas que montar nada, y sin cambiar nada que no hayas "
         "aprobado.", False),
    ]], size=26, font=TITLE_FONT)
    steps = ["Audita tu espacio", "Propone un mapa a tu medida",
             "Pregunta solo lo dudoso", "Aplica por lotes, con deshacer",
             "Mantiene el orden"]
    col_w = (CONTENT_W - 4 * 0.25) / 5
    accent_bar(slide, MARGIN + col_w / 2, 3.43, CONTENT_W - col_w, 0.04)
    for i, step in enumerate(steps):
        x = MARGIN + i * (col_w + 0.25)
        color = PURPLE if i % 2 else CYAN
        number_badge(slide, x + col_w / 2 - 0.35, 3.1, str(i + 1), color=color,
                     size=0.7)
        text(slide, x, 3.95, col_w, 1.0, step, size=18, bold=True,
             font=TITLE_FONT, align=PP_ALIGN.CENTER)
    callout(slide, MARGIN, 5.3, CONTENT_W, 1.25,
            "Para personas no técnicas, también en los planes Free y Plus de "
            "Notion: sin instrucciones ni configuración.")


def hypotheses(prs, number):
    slide = content_slide(prs, "Hipótesis que validaremos", number)
    rows = [
        ("H1", "El desorden en Notion es un problema que quieren resolver",
         "2+ beta testers con una dificultad reciente y concreta"),
        ("H2", "Un espacio ordenado mejora la recuperación, también con IA",
         "De 10 preguntas, mejoran 3+ y empeora 1 como mucho"),
        ("H3", "El flujo guiado supera a pedírselo a Notion AI o a Claude",
         "Menos tiempo y menos correcciones en el mismo espacio"),
        ("H4", "Confían en las sugerencias si pueden revisar y deshacer",
         "70 % aceptadas y menos del 10 % deshechas"),
        ("H5", "Siguen usando Oracle para mantener el orden",
         "La mitad lo vuelve a usar en 4 semanas"),
        ("H6", "La IA deduce una organización propia de cada usuario",
         "La mitad mantiene el mapa con cambios menores"),
    ]
    text(slide, MARGIN + 0.9, 1.4, 6.6, 0.4, "Hipótesis", size=14, bold=True,
         color=MUTED)
    text(slide, MARGIN + 7.8, 1.4, 4.3, 0.4, "Criterio de éxito", size=14,
         bold=True, color=MUTED)
    for i, (code, claim, criterion) in enumerate(rows):
        y = 1.85 + i * 0.8
        color = PURPLE if i % 2 else CYAN
        number_badge(slide, MARGIN, y + 0.04, code, color=color, size=0.6)
        text(slide, MARGIN + 0.9, y, 6.8, 0.7, claim, size=17, bold=True,
             anchor=MSO_ANCHOR.MIDDLE)
        text(slide, MARGIN + 7.8, y, 4.3, 0.7, criterion, size=15, color=MUTED,
             anchor=MSO_ANCHOR.MIDDLE)


def mvp(prs, number):
    slide = content_slide(prs, "Decisión sobre el MVP", number)
    col_w = (CONTENT_W - 0.6) / 3
    columns = [
        ("Construimos", CYAN, [
            "Un asistente que organiza tu Notion:",
            "conectar · auditar · proponer un mapa · preguntar · revisar y "
            "aplicar · deshacer · volver a ejecutar",
        ]),
        ("Modificamos", PURPLE, [
            "Express pasa a ser un asistente de trabajo, más adelante.",
            "De solo leer a escribir en Notion, con aprobación previa.",
            "PARA, de estructura fija a propuesta adaptable.",
        ]),
        ("Posponemos", CYAN, [
            "Asistente de trabajo (Express).",
            "Chat sobre las notas.",
            "Otras fuentes además de Notion.",
            "Priorizar tareas y una app de notas nueva: descartados.",
        ]),
    ]
    for i, (heading, color, body) in enumerate(columns):
        x = MARGIN + i * (col_w + 0.3)
        card(slide, x, 1.6, col_w, 3.4, heading, body, accent=color,
             heading_size=22, body_size=17)
    callout(slide, MARGIN, 5.35, CONTENT_W, 1.1,
            "Alcance a la medida de pocas horas semanales: solo Notion, solo "
            "mover páginas, siempre a petición del usuario.")


def why_ai(prs, number):
    slide = content_slide(prs, "Por qué usamos IA", number)
    text(slide, MARGIN, 1.5, CONTENT_W, 0.9,
         "Clasificar una nota exige entender su contenido. Las reglas fijas no "
         "bastan; un modelo de lenguaje sí puede:", size=19)
    uses = [
        ("Auditar", "por lo que dicen las notas, no por cómo se llaman."),
        ("Adaptarse a cada persona", "deduciendo sus temas y proyectos reales."),
        ("Saber cuándo dudar", "y preguntar solo por lo dudoso."),
        ("Explicar cada propuesta", "para que revisar sea rápido."),
    ]
    col_w = (CONTENT_W - 0.3) / 2
    for i, (heading, body) in enumerate(uses):
        x = MARGIN + (i % 2) * (col_w + 0.3)
        y = 2.45 + (i // 2) * 1.35
        card(slide, x, y, col_w, 1.15, heading, body,
             accent=PURPLE if i % 2 else CYAN, heading_size=19, body_size=15)
    callout(slide, MARGIN, 5.3, CONTENT_W, 1.3, [
        [("Dónde no la usamos: ", True), ("mover, aplicar y deshacer son operaciones directas "
                              "sobre Notion, predecibles y reversibles.", False)],
        [("Cada persona organiza sus notas a su manera: ", True),
         ("la IA se adapta a ella, no al revés.", False)],
    ], size=16)


def next_steps(prs, number):
    slide = content_slide(prs, "Próximos pasos", number)
    steps = [
        ("Construir", "una primera versión que ya escribe en Notion."),
        ("Probar", "con las dos profesoras (H1)."),
        ("Ampliar", "el grupo con usuarios de r/secondbrain y Notion."),
        ("Medir", "con pruebas prácticas (H2 y H3)."),
        ("Decidir", "los siguientes pasos con el equipo."),
    ]
    col_w = (CONTENT_W - 4 * 0.25) / 5
    accent_bar(slide, MARGIN + col_w / 2, 2.13, CONTENT_W - col_w, 0.04)
    for i, (heading, body) in enumerate(steps):
        x = MARGIN + i * (col_w + 0.25)
        color = PURPLE if i % 2 else CYAN
        number_badge(slide, x + col_w / 2 - 0.35, 1.8, str(i + 1), color=color,
                     size=0.7)
        text(slide, x, 2.7, col_w, 0.5, heading, size=21, bold=True,
             font=TITLE_FONT, align=PP_ALIGN.CENTER)
        text(slide, x, 3.25, col_w, 1.3, body, size=16, color=MUTED,
             align=PP_ALIGN.CENTER)
    callout(slide, MARGIN, 5.0, CONTENT_W, 1.5, [
        [("Dos beta testers listas ", True),
         ("para probar la primera versión desde el primer día.", False)],
        "Cada hipótesis tiene un criterio de éxito claro.",
    ], size=19)


def closing(prs, number):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill_background(slide, NAVY)
    slide.shapes.add_picture(str(LOGO_FULL), Inches(SLIDE_W - SLIDE_H), 0,
                             Inches(SLIDE_H), Inches(SLIDE_H))
    text(slide, 0.9, 0.9, 6.6, 1.0, "Listos para construir", size=40,
         color=WHITE, bold=True, font=TITLE_FONT)
    accent_bar(slide, 0.95, 1.95, 2.2, 0.08)
    done = [
        "Usuario objetivo concreto",
        "Conversaciones con usuarios reales",
        "Competencia analizada",
        "Hipótesis con criterios de éxito",
        "MVP decidido y uso de la IA justificado",
    ]
    for i, item in enumerate(done):
        y = 2.4 + i * 0.62
        text(slide, 0.9, y, 0.5, 0.5, "✓", size=22, bold=True,
             color=PURPLE if i % 2 else CYAN)
        text(slide, 1.45, y + 0.03, 5.9, 0.5, item, size=20, color=WHITE)
    text(slide, 0.9, 6.0, 6.4, 0.8, "Gracias. ¿Preguntas?", size=24,
         color=CYAN, font=TITLE_FONT)
