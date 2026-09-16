import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:

    def __init__(self):

        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT"))

        self.email_remitente = os.getenv("EMAIL_REMITENTE")
        self.email_password = os.getenv("EMAIL_PASSWORD")

    def enviar_correo(self, destinatario, curso):

        mensaje = MIMEMultipart()

        mensaje["From"] = self.email_remitente
        mensaje["To"] = destinatario
        mensaje["Subject"] = f"Información del curso: {curso['nombre']}"

        contenido = f"""
Hola,

Has solicitado información sobre el siguiente curso:

Curso: {curso['nombre']}

Descripción:
{curso['descripcion']}

Modalidad: {curso['modalidad']}
Duración: {curso['duracion']}
Costo: ${curso['costo']:,}

Requisitos:
{curso['requisitos']}

Gracias por tu interés.
"""

        mensaje.attach(
            MIMEText(contenido, "plain", "utf-8")
        )

        with smtplib.SMTP(
            self.smtp_host,
            self.smtp_port
        ) as servidor:

            servidor.starttls()

            servidor.login(
                self.email_remitente,
                self.email_password
            )

            servidor.send_message(mensaje)

        return True