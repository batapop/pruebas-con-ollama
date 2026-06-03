# Ejercicio: Generación de Archivos con IA Local

**David Felipe Batanero Molina**
**Código:** 20241020092

---

## Descripción del Ejercicio

Exploración práctica del uso de un agente de IA corriendo localmente mediante **Ollama**, con el objetivo de generar y modificar archivos HTML de forma autónoma a través de herramientas (*tools*) definidas en Python.

---

## Herramientas Utilizadas

- **Ollama** — motor para correr modelos de IA localmente
- **Modelo:** `qwen2.5:3b` — modelo ligero seleccionado por restricción de RAM (6GB)
- **Python** — lenguaje del agente y definición de tools
- **Tinkercad / Navegador** — visualización de resultados

---

## Archivos del Repositorio

| Archivo | Descripción |
|---|---|
| `agente.py` | Script principal del agente con definición de tools de lectura y escritura de archivos |
| `index.html` / intentos anteriores | Versiones generadas durante el proceso |
| `index_beta.html` | **Mejor resultado obtenido** — último intento funcional antes de que el agente dejara de responder correctamente |

---

## Proceso

1. Se configuró Ollama con el modelo `qwen2.5:3b`
2. Se definieron dos tools en Python: `leer_archivo` y `escribir_archivo`
3. Se le instruyó al agente mediante un prompt detallado para generar una página web temática de conejos con paleta pastel (morado y verde)
4. Se realizaron múltiples iteraciones ajustando el prompt para mejorar el resultado visual

---

## Observaciones

- Cada intento de generación tomaba aproximadamente **15 minutos** dado el hardware limitado (AMD Ryzen 3, 6GB RAM, GPU integrada)
- El modelo en algunos intentos ignoró las tools y respondió con texto plano en lugar de escribir el archivo directamente
- Se implementó un fallback en el script para detectar HTML en la respuesta y guardarlo manualmente
- A partir de cierto punto el agente dejó de generar resultados útiles — causa no determinada (posiblemente contexto acumulado o temperatura del modelo)
- **`index_beta.html` representa el mejor resultado alcanzado** antes de que el comportamiento se volviera inconsistente

---

## Conclusión

El ejercicio permitió comprender el flujo básico de un agente de IA local con tool use: definición de herramientas, ciclo de llamada y respuesta, y manejo de casos donde el modelo no sigue las instrucciones esperadas. Las limitaciones de hardware influyeron directamente en los tiempos de respuesta y en la estabilidad del modelo.