def mensaje_bienvenida():
    return (
        "👋 ¡Hola! Bienvenido al sistema de citas.\n\n"
        "¿Qué deseas hacer?\n"
        "1️⃣ Agendar una cita\n"
        "2️⃣ Consultar tu cita\n\n"
        "Responde con 1 o 2."
    )


def mensaje_seleccion_doctor(doctores):
    msg = "🩺 ¿Con qué doctor deseas agendar?\n\n"
    for i, doc in enumerate(doctores, 1):
        msg += f"{i}. {doc['name']}\n"
    msg += "\nEscribe el número del doctor que elijas."
    return msg


def mensaje_pedir_nombre():
    return "📛 ¿Cuál es tu nombre completo?"


def mensaje_pedir_fecha():
    return (
        "📅 ¿Qué día te gustaría agendar tu cita?\n"
        "Indica la fecha en formato DD/MM/AAAA. Ejemplo: 30/04/2025"
    )


def mensaje_pedir_hora():
    return "🕒 ¿A qué hora? Usa el formato HH:MM en 24 horas. Ejemplo: 17:40"


def mensaje_confirmacion(nombre, fecha, hora, doctor):
    return (
        f"✅ ¡Gracias, {nombre}!\n"
        f"Tu cita con {doctor} ha sido agendada para el {fecha} a las {hora}."
    )


def mensaje_fecha_no_disponible():
    return "❌ Esa fecha no está disponible. ¿Puedes proporcionar otra fecha?"


def mensaje_hora_no_disponible():
    return "⏰ Esa hora no está disponible. ¿Puedes dar otra hora?"


def mensaje_consulta_nombre():
    return "🔍 Por favor, indícame tu nombre completo para buscar tu cita."


def mensaje_cita_encontrada(nombre, fecha, hora, doctor):
    return (
        f"📋 {nombre}, tu cita está agendada con {doctor} para el {fecha} a las {hora}."
    )


def mensaje_cita_no_encontrada():
    return "😕 No encontré ninguna cita registrada con ese nombre."


def mensaje_cancelacion():
    return "👌 Entendido. Si necesitas algo más, solo escribe 'hola'. ¡Que tengas un buen día!"


def mensaje_formato_invalido():
    return (
        "⚠️ Parece que el formato no es correcto.\n"
        "Recuerda:\n- Fecha: DD/MM/AAAA\n- Hora: HH:MM en formato 24 horas."
    )


def mensaje_reiniciar():
    return "🔁 Escribe 'hola' para comenzar nuevamente."
