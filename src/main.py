import os
import requests

from dotenv import load_dotenv

from agente import Agente
from email_service import EmailService


load_dotenv()


# CARGAR CURSOS DESDE GITHUB


cursos_url = os.getenv("CURSOS_URL")

response = requests.get(cursos_url)

response.raise_for_status()

cursos = response.json()


print("Cursos cargados:", len(cursos))



# CREAR AGENTE


agente = Agente(cursos)
email_service = EmailService()

print("Cursos cargados:", len(cursos))
print("Agente creado correctamente.")

print("\nEscribe 'salir' para terminar.")
print("-" * 40)



# BUCLE PRINCIPAL


while True:

    user_input = input("\nTú: ").strip()

    if not user_input:
        continue

    if user_input.lower() in ("salir", "exit"):

        print("¡Hasta luego!")

        break

    # Guardar mensaje del usuario
    agente.agregar_usuario(user_input)

    # Consultar Gemini
    respuesta = agente.consultar()

    agente.agregar_modelo(respuesta)

    datos = agente.procesar_respuesta(respuesta)

    if datos["accion"] == "enviar_correo":

        curso = next(
            curso for curso in cursos
            if curso["id"] == datos["curso_id"]
        )

        email_service.enviar_correo(
            datos["correo"],
            curso
        )

        print("\nAsistente: El correo fue enviado correctamente.")

    else:

        print(f"\nAsistente: {datos['respuesta']}")
    
    
    #print("\nJSON recibido:")
    #print(datos)

    #if datos["accion"] == "enviar_correo":

    #    curso = next(
    #        curso for curso in cursos
    #        if curso["id"] == datos["curso_id"]
    #   )

    #    email_service.enviar_correo(
    #        datos["correo"],
    #        curso
    #    )

    #    print("\nAsistente: El correo fue enviado correctamente.")

    #else:

    #    print(f"\nAsistente: {datos['respuesta']}")