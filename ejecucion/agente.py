import ollama
import json
import os

# --- Definición de las tools ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "leer_archivo",
            "description": "Lee el contenido de un archivo de texto",
            "parameters": {
                "type": "object",
                "properties": {
                    "ruta": {
                        "type": "string",
                        "description": "Ruta del archivo a leer"
                    }
                },
                "required": ["ruta"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "escribir_archivo",
            "description": "Crea o sobreescribe un archivo con el contenido dado",
            "parameters": {
                "type": "object",
                "properties": {
                    "ruta": {
                        "type": "string",
                        "description": "Ruta del archivo"
                    },
                    "contenido": {
                        "type": "string",
                        "description": "Contenido a escribir en el archivo"
                    }
                },
                "required": ["ruta", "contenido"]
            }
        }
    }
]

# --- Implementación real de las tools ---
def leer_archivo(ruta):
    nombre = os.path.basename(ruta)
    ruta_segura = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre)
    if not os.path.exists(ruta_segura):
        return f"Error: el archivo '{nombre}' no existe."
    with open(ruta_segura, "r", encoding="utf-8") as f:
        return f.read()

def escribir_archivo(ruta, contenido):
    # Fuerza que el archivo se guarde en la misma carpeta del script
    nombre = os.path.basename(ruta)
    ruta_segura = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre)
    with open(ruta_segura, "w", encoding="utf-8") as f:
        f.write(contenido)
    return f"Archivo '{nombre}' escrito correctamente."

def ejecutar_tool(nombre, args):
    if nombre == "leer_archivo":
        return leer_archivo(args["ruta"])
    elif nombre == "escribir_archivo":
        return escribir_archivo(args["ruta"], args["contenido"])
    return "Tool desconocida."

# --- Loop del agente ---
def agente(prompt_usuario):
    messages = [{"role": "user", "content": prompt_usuario}]

    while True:
        response = ollama.chat(
            model="qwen2.5:3b",
            messages=messages,
            tools=tools
        )

        msg = response["message"]
        messages.append(msg)

        if msg.get("tool_calls"):
            for tool_call in msg["tool_calls"]:
                nombre = tool_call["function"]["name"]
                args = tool_call["function"]["arguments"]
                
                print(f"[Tool] Ejecutando: {nombre}({args})")
                resultado = ejecutar_tool(nombre, args)
                
                messages.append({
                    "role": "tool",
                    "content": resultado
                })
        else:
            # Si el modelo respondió con texto pero contiene HTML, lo guardamos directo
            contenido = msg["content"]
            if "<!DOCTYPE" in contenido or "<html" in contenido:
                print("[Info] El modelo respondió con código directo, guardando archivo...")
                resultado = escribir_archivo("index.html", contenido)
                print(resultado)
            else:
                print("\n[Respuesta]:", contenido)
            break
# --- Usar el agente ---
agente("""
Usa la tool escribir_archivo para crear index.html. Escribe en el archivo este contenido HTML completo:

INSTRUCCIONES IMPORTANTES:
- Genera SOLO código HTML puro
INSTRUCCIONES IMPORTANTES:
- Genera SOLO el código HTML puro, sin explicaciones ni texto adicional
- No uses bloques markdown ni backticks
- El archivo debe empezar exactamente con <!DOCTYPE html> y terminar con </html>

Crea un archivo index.html con una página web temática de conejos. Sin imágenes, solo emojis y texto.

ESTILO VISUAL:
- Paleta pastel: morado suave (#E8D5F5), verde menta (#C8F0E0), morado oscuro (#9B7FC7) para textos y acentos
- Fondo general de la página: verde menta pastel (#C8F0E0)
- Google Fonts: 'Nunito' para todo el texto
- Tarjetas con border-radius: 16px, padding: 24px, ancho fijo 260px
- Sombras suaves en tarjetas: box-shadow: 0 4px 12px rgba(155, 127, 199, 0.2)
- Todo el CSS dentro del mismo HTML, solo fuente externa de Google Fonts

SECCIONES:

1. HEADER:
   - Fondo degradado de morado suave a verde menta (#E8D5F5 a #C8F0E0)
   - Emoji grande centrado: 🐰
   - Título 'Bunny World' en morado oscuro, fuente grande
   - Subtítulo pequeño: 'Un lugar suave y esponjoso'
   - Padding generoso arriba y abajo

2. SECCIÓN 'NUESTROS CONEJOS':
   - Fondo blanco con 60% de opacidad
   - Título centrado: '🐇 Nuestros Conejos'
   - 3 tarjetas en fila, centradas, con flexbox, flex-wrap: wrap, gap: 20px, justify-content: center
   - Tarjeta 1: fondo #E8D5F5 — nombre 'Mochi' — '🐇' arriba — "Tímido y esponjoso, ama dormir en rincones"
   - Tarjeta 2: fondo #C8F0E0 — nombre 'Caramelo' — '🐇' arriba — "Curioso y glotón, siempre busca zanahorias"
   - Tarjeta 3: fondo #F0E8FF — nombre 'Nube' — '🐇' arriba — "Juguetón y veloz, nunca se queda quieto"
   - Nombre en negrita, descripción en texto pequeño gris suave

3. SECCIÓN 'CURIOSIDADES':
   - Fondo #E8D5F5 suave
   - Título centrado: '🌿 Curiosidades'
   - Lista sin bullets nativos, cada item con emoji al inicio: 🥕 🌿 💤 🐾
   - 4 curiosidades reales sobre conejos
   - Texto centrado, ancho máximo 600px, centrado en la página

4. FOOTER:
   - Fondo #9B7FC7
   - Texto centrado en blanco: 'Hecho con 🐰 y amor · 2025'
   - Padding 20px

ANIMACIONES:
- Hover en tarjetas: transform translateY(-4px), transición 0.3s ease
- Header: animación fadeIn de 1s al cargar (opacity 0 a 1)

Todo en un solo archivo index.html con CSS embebido. Nada fuera del HTML.
""")