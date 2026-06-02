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
Crea un archivo index.html con una página web temática de conejos. Sin imágenes, solo emojis y texto.

ESTILO VISUAL:
- Paleta pastel: morado suave (#E8D5F5), verde menta (#C8F0E0), blanco cremoso (#FFFAF5), morado oscuro (#9B7FC7) para textos y acentos
- Google Fonts: 'Nunito' para todo el texto
- Tarjetas con border-radius: 16px y sombras suaves
- Fondo blanco cremoso (#FFFAF5)
- Todo el CSS dentro del mismo HTML, solo fuente externa de Google Fonts

SECCIONES:

1. HEADER:
   - Fondo degradado de morado a verde pastel
   - Emoji grande centrado: 🐰
   - Título: 'Bunny World'
   - Subtítulo pequeño: 'Un lugar suave y esponjoso'

2. SECCIÓN 'NUESTROS CONEJOS':
   - Título de sección centrado con 🐇
   - 3 tarjetas en fila con flexbox:
     * Mochi — fondo morado pastel — "Tímido y esponjoso, ama dormir en rincones"
     * Caramelo — fondo verde pastel — "Curioso y glotón, siempre busca zanahorias"
     * Nube — fondo morado pastel más claro — "Juguetón y veloz, nunca se queda quieto"
   - Cada tarjeta: emoji 🐇 arriba, nombre en negrita, descripción pequeña

3. SECCIÓN 'CURIOSIDADES':
   - Fondo verde pastel suave
   - 4 curiosidades reales sobre conejos
   - Lista con emojis como bullets: 🥕 🌿 💤 🐾

4. FOOTER:
   - Fondo morado pastel
   - Texto centrado: 'Hecho con 🐰 y amor · 2025'

ANIMACIONES:
- Hover en tarjetas: suben suavemente translateY -4px, transición 0.3s
- Header: fadeIn simple al cargar

Todo en un solo archivo index.html con CSS embebido.
""")