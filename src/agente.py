import os
import json
import requests


class Agente:

    def __init__(self, cursos):

        self.cursos = cursos

        self.api_key = os.getenv("GEMINI_API_KEY")

        self.modelo = "gemini-3.5-flash-lite"

        self.url = (
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/{self.modelo}:generateContent"
            f"?key={self.api_key}"
        )

        # Memoria de la conversación
        self.messages = []

        self.system_prompt = self.crear_system_prompt()


    # SYSTEM PROMPT


    def crear_system_prompt(self):

        cursos_json = json.dumps(
            self.cursos,
            ensure_ascii=False,
            indent=2
        )

        return f"""
Eres un asistente encargado de asesorar
a los usuarios sobre cursos online.

Debes responder siempre en español.

Solo puedes utilizar la información de los
cursos proporcionados.

No inventes cursos, precios, duración,
modalidad ni requisitos.

Sé claro y conciso.

Tu función es:

1. Informar sobre los cursos disponibles.
2. Responder preguntas sobre los cursos.
3. Identificar cuando el usuario está interesado
   en inscribirse.
4. Solicitar el correo electrónico del usuario
   cuando quiera recibir información para la
   inscripción.
5. Cuando tengas un curso seleccionado y un correo
   electrónico válido, debes generar una orden
   estructurada para enviar la información.

IMPORTANTE:

No envías correos directamente.

Cuando el usuario quiera inscribirse y ya tengas
su correo electrónico, debes responder utilizando
EXACTAMENTE este formato JSON:

{{
    "accion": "enviar_correo",
    "curso_id": 0,
    "correo": "correo@ejemplo.com",
    "respuesta": "Se enviará la información del curso a tu correo."
}}

El campo "curso_id" debe corresponder al ID real
del curso.

Si todavía NO tienes suficiente información para
enviar el correo, utiliza:

{{
    "accion": "ninguna",
    "curso_id": 0,
    "correo": "",
    "respuesta": "Tu respuesta normal al usuario."
}}

Cuando la acción sea "ninguna", responde normalmente.

Cuando la acción sea "enviar_correo", NO agregues
texto fuera del JSON.

Estos son los cursos disponibles:

{cursos_json}
"""


    # AGREGAR MENSAJE DEL USUARIO

    def agregar_usuario(self, mensaje):

        self.messages.append({
            "role": "user",
            "parts": [
                {
                    "text": mensaje
                }
            ]
        })

    # AGREGAR RESPUESTA DEL MODELO

    def agregar_modelo(self, mensaje):

        self.messages.append({
            "role": "model",
            "parts": [
                {
                    "text": mensaje
                }
            ]
        })

    # CONSULTAR GEMINI

    def consultar(self):

        datos = {

            "system_instruction": {
                "parts": [
                    {
                        "text": self.system_prompt
                    }
                ]
            },

            "contents": self.messages,

            "generationConfig": {
                "responseMimeType": "application/json"
            },
        }

        response = requests.post(
            self.url,
            json=datos,
            timeout=60
        )


        if response.status_code != 200:
            print("\nERROR DE GEMINI:")
            print(response.text)

        resultado = response.json()

        texto = (
            resultado["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

        return texto
    

    # PROCESAR RESPUESTA


    def procesar_respuesta(self, texto):

        try:

            datos = json.loads(texto)

            if "accion" in datos:

                return datos

        except json.JSONDecodeError:

            pass

        return {
            "accion": "ninguna",
            "curso_id": 0,
            "correo": "",
            "respuesta": texto
        }