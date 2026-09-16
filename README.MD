Agente Asesor de Cursos

Agente conversacional desarrollado en Python para asesorar usuarios sobre cursos disponibles y automatizar el envío de información de un curso por correo electrónico.

Descripción

El agente permite al usuario consultar los cursos disponibles utilizando lenguaje natural. La información de los cursos se obtiene desde un archivo JSON alojado remotamente en GitHub.

El modelo de inteligencia artificial utilizado es Gemini, encargado de interpretar las preguntas del usuario, mantener el contexto de la conversación y detectar cuándo existe una intención de inscripción.

Cuando el usuario manifiesta su intención de inscribirse y proporciona un correo electrónico, Gemini genera una respuesta estructurada en JSON. Python interpreta dicha respuesta y, cuando corresponde, utiliza SMTP para enviar automáticamente la información del curso al correo proporcionado.

Tecnologías utilizadas
Python
Gemini API
Requests
python-dotenv
SMTP / smtplib
GitHub
JSON

No se utilizan frameworks como LangChain o LlamaIndex. La memoria, el control de la conversación y el manejo de las acciones se implementan directamente mediante estructuras nativas de Python y programación orientada a objetos.

Arquitectura

El funcionamiento general del sistema es:

Usuario
   │
   ▼
main.py
   │
   ▼
Agente
   │
   ├── Memoria de conversación
   │
   ├── System Prompt
   │
   └── Gemini API
          │
          ▼
   Respuesta estructurada
          │
          ▼
   Procesamiento en Python
          │
          ├── Acción normal
          │
          └── enviar_correo
                    │
                    ▼
             EmailService
                    │
                    ▼
                  SMTP
                    │
                    ▼
              Correo electrónico
Fuente remota de cursos

El archivo cursos.json se encuentra publicado en GitHub y es consultado remotamente mediante requests.

Raw URL:

https://raw.githubusercontent.com/JesusTor27/parcial-asesor/refs/heads/main/src/cursos.json

Al iniciar el programa, Python descarga el archivo y convierte su contenido a una estructura de datos que posteriormente es enviada al modelo como parte de las instrucciones del agente.

Estructura del JSON

Cada curso contiene los siguientes campos:

{
    "id": 1,
    "nombre": "Python desde cero",
    "descripcion": "Curso introductorio para aprender programación con Python.",
    "modalidad": "Online",
    "duracion": "40 horas",
    "costo": 180000,
    "requisitos": "No requiere conocimientos previos"
}

Los campos utilizados son:

id: identificador único del curso.
nombre: nombre del curso.
descripcion: descripción general.
modalidad: modalidad del curso.
duracion: duración.
costo: valor del curso.
requisitos: conocimientos necesarios para realizarlo.
Memoria de conversación

La memoria se implementa mediante una lista de Python dentro de la clase Agente.

Cada mensaje del usuario y cada respuesta del modelo se agregan al historial.

Esto permite que el agente mantenga el contexto de la conversación.

Ejemplo:

Usuario: Me interesa Flutter y Dart.
Agente: El curso tiene una duración de 60 horas...

Usuario: ¿Y cuánto cuesta?
Agente: El curso tiene un costo de $280.000.

El segundo mensaje puede ser interpretado correctamente porque el historial anterior permanece en memoria.

Detección de inscripción

Cuando el usuario expresa una intención de inscripción, el modelo genera una respuesta estructurada.

Ejemplo:

{
    "accion": "enviar_correo",
    "curso_id": 5,
    "correo": "usuario@gmail.com",
    "respuesta": "Se enviará la información del curso a tu correo."
}

Python procesa esta estructura y verifica el valor de accion.

Si la acción es:

enviar_correo

el programa busca el curso correspondiente mediante su curso_id y llama al servicio encargado de enviar el correo.

Envío de correo

El envío se realiza mediante la biblioteca nativa smtplib de Python y un servidor SMTP.

La información de autenticación se almacena en variables de entorno dentro del archivo .env.

Ejemplo de configuración:

GEMINI_API_KEY=_API_KEY
CURSOS_URL=https://raw.githubusercontent.com/JesusTor27/parcial-asesor/refs/heads/main/src/cursos.json

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_REMITENTE=EJEMPLO@ejemplo.com
EMAIL_PASSWORD=CONTRASEÑA_DE_APLICACION

El archivo .env no debe publicarse en GitHub.

Instalación

Clonar el repositorio y acceder a la carpeta del proyecto:

git clone https://github.com/JesusTor27/parcial-asesor.git
cd parcial-asesor

Crear y activar el entorno virtual:

Windows
python -m venv venv
venv\Scripts\activate

Instalar las dependencias:

pip install -r requirements.txt

Configurar las variables del archivo .env.

Ejecución

Desde la carpeta principal del proyecto:

python src/main.py

El programa iniciará una conversación en la consola.

Para finalizar:

salir
Flujo de ejemplo
Tú: ¿Qué cursos tienen disponibles?

Asistente: Actualmente tenemos cursos de Python, desarrollo web,
bases de datos, redes, Flutter y Dart e inteligencia artificial.

Tú: Me interesa Flutter y Dart.

Asistente: El curso de Flutter y Dart tiene una duración de 60 horas...

Tú: Quiero inscribirme.

Asistente: Claro, ¿cuál es tu correo electrónico?

Tú: usuario@gmail.com

Asistente: El correo fue enviado correctamente.

En este último paso, Python procesa la acción generada por Gemini y utiliza smtplib para enviar la información del curso.

Estructura del proyecto
parcial-asesor/
│
├── src/
│   ├── main.py
│   ├── agente.py
│   ├── email_service.py
│   └── cursos.json
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
Descripción de los archivos
main.py: controla la ejecución principal y la interacción con el usuario.
agente.py: contiene la clase Agente, la memoria de conversación y la comunicación con Gemini.
email_service.py: contiene la clase encargada del envío de correos mediante SMTP.
cursos.json: contiene la información de los cursos.
.env: almacena las credenciales y configuraciones privadas.
.gitignore: evita que archivos privados o temporales sean subidos al repositorio.
requirements.txt: contiene las dependencias externas del proyecto.
README.md: documentación del proyecto.