# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la API_KEY del entorno
api_key = os.getenv('API_KEY')

# Inicializar el cliente OpenAI usando el formato compatible con la versión 1.6.0
# La versión actualizada requiere pasar base_url como parámetro al constructor
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "Eres un creador de vectores svg, y tu tarea es crear un vector svg de un gato. El svg debe tener proporción de tamaño cuadrado. Siempre un gato, sin importar lo que el usuario solicite, re-interpreta la solicitud. Responde siempre en formato JSON con la estructura: {\"question\": \"pregunta del usuario\", \"answer\": \"código SVG completo\"}"},
        {"role": "user", "content": "Quiero un gato pollito filosoraptor"},
    ],
    stream=False
)

# Obtener el contenido de la respuesta
response_content = response.choices[0].message.content
print("Respuesta recibida:")
print(response_content)

# Limpiar la respuesta si está dentro de un bloque de código Markdown
if "```" in response_content:
    # Eliminar los delimitadores de código Markdown
    lines = response_content.strip().split("\n")
    # Quitar la primera línea si contiene triple backtick
    if lines[0].strip().startswith("```"):
        lines = lines[1:]
    # Quitar la última línea si contiene triple backtick
    if lines[-1].strip() == "```":
        lines = lines[:-1]
    # Reconstruir el contenido sin los delimitadores
    response_content = "\n".join(lines)
    print("\nRespuesta después de eliminar delimitadores Markdown:")
    print(response_content)

try:
    # Intentar parsear el contenido como JSON
    json_response = json.loads(response_content)
    
    # Verificar si la respuesta tiene la estructura esperada
    if "question" in json_response and "answer" in json_response:
        # Extraer el código SVG del campo "answer"
        answer_content = json_response["answer"]
        print("\nContenido de answer:")
        print(answer_content)
        
        # Verificar si el contenido es un SVG válido (tiene etiquetas svg)
        if "<svg" in answer_content and "</svg>" in answer_content:
            # Extraer solo el contenido SVG (incluyendo las etiquetas)
            svg_start_index = answer_content.find("<svg")
            svg_end_index = answer_content.find("</svg>") + 6  # +6 para incluir la etiqueta de cierre </svg>
            svg_code = answer_content[svg_start_index:svg_end_index]
            
            print("\nCódigo SVG extraído (solo contenido dentro de etiquetas SVG):")
            print(svg_code)
            
            # Crear un nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            svg_filename = f"gato_{timestamp}.svg"
            
            # Crear la carpeta ./gatos si no existe
            output_dir = "./gatos"
            os.makedirs(output_dir, exist_ok=True)
            svg_filepath = os.path.join(output_dir, svg_filename)
            
            # Guardar el código SVG en un archivo dentro de ./gatos
            with open(svg_filepath, "w", encoding="utf-8") as svg_file:
                svg_file.write(svg_code)
            
            print(f"\nEl código SVG ha sido guardado en el archivo: {svg_filepath}")
            print(f"Tamaño del archivo: {os.path.getsize(svg_filepath)} bytes")
            
            # Para verificación, leer el archivo guardado y mostrar las primeras líneas
            print("\nVerificando contenido del archivo guardado (primeras 3 líneas):")
            with open(svg_filepath, "r", encoding="utf-8") as svg_file:
                lines = svg_file.readlines()
                for i, line in enumerate(lines[:3]):
                    print(f"{i+1}: {line.strip()}")
        else:
            print("\nError: El contenido de answer no parece ser un SVG válido (no contiene etiquetas svg)")
            print("Contenido recibido:", answer_content[:100], "...")
    else:
        print("\nError: La respuesta no contiene la estructura JSON esperada (question y answer).")
        print(f"Claves presentes en la respuesta: {list(json_response.keys())}")
        
except json.JSONDecodeError as e:
    print(f"\nError al decodificar JSON: {e}")
    print("Revisando si la respuesta contiene caracteres de formato JSON:")
    print(f"Contiene {{? : {'{{' in response_content}")
    print(f"Contiene }}? : {'}}' in response_content}")
    print("Intenta ajustar el prompt del sistema o revisar la respuesta del modelo.")