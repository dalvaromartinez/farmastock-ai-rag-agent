# FarmaStock AI

**FarmaStock AI** es un asistente experto desarrollado como proyecto final de IA Generativa. Su objetivo es responder preguntas sobre optimización de stock en farmacia comunitaria utilizando una arquitectura basada en **Gemini**, **RAG**, **ChromaDB**, **LangGraph** y **memoria conversacional**.

El proyecto se ha implementado como un MVP funcional en notebook, con una base de conocimiento propia formada por documentos Markdown diseñados específicamente para alimentar un sistema RAG.

---

## 1. Descripción breve del proyecto

FarmaStock AI es un agente conversacional especializado en la gestión logística del inventario en farmacia comunitaria.

El asistente puede responder preguntas sobre:

- Rotación de stock.
- Cobertura de stock.
- Stock mínimo, máximo y stock de seguridad.
- Punto de pedido.
- Demanda histórica.
- Lead time o plazo de reposición.
- Riesgo de rotura.
- Sobrestock.
- Clasificación ABC/XYZ.
- Interpretación de movimientos de inventario.

El agente utiliza una base de conocimiento vectorial propia y recupera contexto documental antes de generar cada respuesta. Esto permite que sus respuestas estén alineadas con el dominio del proyecto y no dependan únicamente del conocimiento general del modelo de lenguaje.

---

## 2. Objetivo del agente

El objetivo principal de FarmaStock AI es actuar como un asistente técnico-formativo para apoyar el análisis de stock en farmacia comunitaria.

El agente está diseñado para:

- Explicar conceptos básicos y aplicados de gestión de inventario.
- Ayudar a interpretar métricas de reposición.
- Identificar criterios de riesgo de rotura o sobrestock.
- Explicar la utilidad de la clasificación ABC/XYZ.
- Interpretar movimientos de stock como ventas, entradas, recuentos, ajustes y modificaciones manuales.
- Mantener una conversación coherente entre turnos mediante memoria conversacional.

El agente no toma decisiones automáticas de compra. Su función es apoyar el análisis, no sustituir la revisión humana.

---

## 3. Dominio elegido y justificación

El dominio elegido es:

> **Optimización de stock en farmacia comunitaria**

Se ha elegido este dominio porque es específico, acotado y adecuado para un sistema RAG. Permite construir una base documental propia, generar preguntas de prueba claras y demostrar el funcionamiento de un agente experto sin utilizar datos reales sensibles.

Además, es un dominio con suficiente profundidad técnica para justificar el uso de IA generativa:

- Tiene conceptos propios.
- Requiere interpretación contextual.
- Permite combinar reglas de negocio y razonamiento.
- Es adecuado para evaluar recuperación documental.
- Permite demostrar memoria conversacional con preguntas de seguimiento.

El dominio se centra en la parte logística y analítica de la farmacia comunitaria, no en la parte clínica.

---

## 4. Límites del agente

FarmaStock AI tiene límites explícitos para mantener el proyecto seguro, defendible y alineado con su dominio.

El agente **no debe**:

- Dar consejo clínico.
- Recomendar tratamientos.
- Recomendar medicamentos.
- Sustituir la revisión humana ni el criterio profesional de la persona responsable de la gestión del inventario.
- Usar datos reales sensibles.
- Trabajar con información identificable de pacientes, personas usuarias, proveedores, ventas reales o farmacias concretas.
- Inventar cifras de ventas, stock, demanda, márgenes, proveedores o datos reales.
- Tomar decisiones automáticas de compra.
- Responder con seguridad cuando el contexto recuperado sea insuficiente.

Si la pregunta está fuera del dominio, el agente debe indicarlo claramente.

Si el contexto recuperado no es suficiente, debe explicar qué dato faltaría para responder mejor.

---

## 5. Base de conocimiento

La base de conocimiento está formada por **4 documentos propios en formato Markdown**, redactados específicamente para este proyecto.

Los documentos se encuentran en la carpeta:

```text
data/raw/
```

Los documentos incluidos son:

```text
data/raw/01_fundamentos_stock_farmacia.md
data/raw/02_metricas_reposicion_farmacia.md
data/raw/03_clasificacion_abc_xyz_farmacia.md
data/raw/04_interpretacion_movimientos_stock.md
```

### 5.1. Documento 1

```text
01_fundamentos_stock_farmacia.md
```

Contiene los conceptos base de la gestión de stock:

- Tipos de stock.
- Rotación.
- Cobertura.
- Stock mínimo.
- Stock máximo.
- Stock de seguridad.
- Punto de pedido.
- Roturas.
- Sobrestock.
- Límites del análisis de stock.

### 5.2. Documento 2

```text
02_metricas_reposicion_farmacia.md
```

Contiene métricas y criterios aplicados de reposición:

- Demanda histórica.
- Venta media diaria, semanal y mensual.
- Cobertura en días.
- Lead time.
- Punto de pedido aplicado.
- Riesgo de rotura.
- Detección de sobrestock.
- Priorización de revisión manual.
- Datos necesarios antes de recomendar reposición.

### 5.3. Documento 3

```text
03_clasificacion_abc_xyz_farmacia.md
```

Contiene la explicación de la clasificación ABC/XYZ aplicada al inventario:

- Clasificación ABC.
- Clasificación XYZ.
- Matriz ABC/XYZ.
- Interpretación de productos AX, AY, AZ.
- Interpretación de productos BX, BY, BZ.
- Interpretación de productos CX, CY, CZ.
- Uso de ABC/XYZ para priorizar revisiones.
- Límites de la clasificación.

### 5.4. Documento 4

```text
04_interpretacion_movimientos_stock.md
```

Contiene reglas para interpretar movimientos de inventario:

- Movimientos de venta.
- Movimientos de compra o entrada.
- Recuentos.
- Ajustes.
- Modificaciones manuales.
- Devoluciones y anulaciones.
- Stock resultante.
- Diferencia entre informes comerciales y movimientos operativos.
- Diferencia entre unidades del movimiento, stock anterior, stock posterior y delta.
- Reglas de negocio para FarmaStock AI.

### 5.5. Datos reales

Los documentos han sido redactados específicamente para este MVP, con un enfoque técnico-formativo y sin incorporar datos reales de una farmacia concreta.

Los documentos **no contienen datos reales** de pacientes, personas usuarias, proveedores, ventas, recetas ni farmacias concretas.

Todos los ejemplos incluidos son genéricos y tienen finalidad formativa. Esta decisión permite construir y probar el sistema RAG sin comprometer privacidad, confidencialidad ni información sensible.

---

## 6. Arquitectura del sistema

La arquitectura general del sistema es:

```text
Documentos Markdown
        ↓
Extracción de metadatos YAML
        ↓
Extracción de secciones Markdown
        ↓
Limpieza básica del texto
        ↓
Chunking con metadatos
        ↓
Gemini Embeddings
        ↓
ChromaDB
        ↓
Retriever
        ↓
LangGraph
        ↓
Gemini como LLM
        ↓
Memoria conversacional
        ↓
Función de chat en notebook
        ↓
Interfaz Streamlit opcional para demo

```

El flujo permite que el agente recupere primero fragmentos relevantes de la base documental y después genere una respuesta usando Gemini.
La interfaz Streamlit no modifica la arquitectura principal del MVP. Actúa como una capa visual opcional para facilitar la demo oral, cargando la base vectorial persistente ya creada desde el notebook.

---

## 7. Decisiones técnicas

### 7.1. Markdown como formato documental

Se ha elegido Markdown porque es un formato sencillo, legible y fácil de procesar.

Permite estructurar los documentos con títulos, secciones, ejemplos, fórmulas conceptuales y bloques de texto claros.

Además, facilita la extracción de secciones mediante encabezados `##`.

---

### 7.2. Metadatos YAML

Cada documento incluye una cabecera YAML con metadatos como:

```yaml
title: "..."
document_id: "..."
version: "1.0"
domain: "Optimización de stock en farmacia comunitaria"
use_in_rag: true
contains_real_data: false
```

Estos metadatos se conservan durante el procesamiento y se propagan a cada sección y chunk.

Esto permite mejorar la trazabilidad del RAG, identificar el origen de cada fragmento recuperado y justificar que la base documental no contiene datos reales sensibles.

---

### 7.3. Extracción de secciones

Los documentos se dividen inicialmente por secciones Markdown usando encabezados de nivel 2:

```text
##
```

Esto permite mantener una segmentación semántica antes de aplicar el chunking por tamaño.

---

### 7.4. Exclusión de secciones de preguntas

Las secciones tituladas:

```text
Preguntas que puede responder este documento
```

se han excluido de la indexación.

La razón es evitar que el retriever recupere preguntas literales en lugar de contenido explicativo. Estas secciones son útiles para diseño y validación, pero no aportan tanta información técnica como las definiciones, ejemplos y reglas de negocio.

---

### 7.5. Chunking

La configuración de chunking utilizada es:

```text
chunk_size = 1000
chunk_overlap = 150
```

Esta configuración busca mantener juntos:

- Definición del concepto.
- Explicación aplicada.
- Ejemplo sencillo.
- Advertencia o límite de uso.

Cada chunk conserva metadatos del documento, de la sección y del propio fragmento.

---

### 7.6. Gemini Embeddings

Para vectorizar los documentos se usan embeddings de Gemini:

```text
models/gemini-embedding-001
```

En la ejecución del notebook, la prueba de embedding generó vectores de dimensión:

```text
3072
```

Este paso permite transformar los chunks documentales en representaciones vectoriales para que ChromaDB pueda recuperar fragmentos relevantes mediante similitud semántica.

---

### 7.7. Indexación por lotes

La indexación en ChromaDB se realiza por lotes para evitar problemas con los límites de frecuencia de la API de Gemini Embeddings.

Durante el desarrollo del MVP se detectaron límites de cuota por minuto, por lo que se implementó una carga por lotes con pausas entre llamadas. Esta decisión permite crear la base vectorial de forma más estable y reproducible.

---

### 7.8. ChromaDB persistente

La base vectorial se almacena de forma persistente en:

```text
chroma_db/
```

La colección utilizada se llama:

```text
farmastock_ai_docs
```

---

### 7.9. Retriever

El retriever se configura con búsqueda por similitud semántica:

```text
search_type = "similarity"
k = 4
```

Esto significa que para cada pregunta se recuperan los 4 chunks más relevantes de la base vectorial.

---

### 7.10. LLM

El modelo de lenguaje utilizado para generar respuestas es:

```text
gemini-2.5-flash
```

La temperatura utilizada es baja:

```text
temperature = 0.2
```

Esto favorece respuestas más estables, concretas y menos creativas.

---

### 7.11. Justificación del system prompt

El system prompt se ha diseñado para acotar el comportamiento del agente al dominio de optimización de stock en farmacia comunitaria.

Sus objetivos principales son:

- Limitar las respuestas al ámbito logístico del inventario.
- Obligar al agente a usar el contexto recuperado desde ChromaDB como fuente principal.
- Indicar claramente cuando el contexto recuperado no sea suficiente.
- Evitar consejo clínico o recomendación de medicamentos.
- Evitar que el modelo invente cifras de ventas, stock, demanda, márgenes, proveedores o datos reales.
- Mantener un tono claro, profesional y orientado a la demo académica.

Esta decisión es importante porque el dominio elegido pertenece al entorno farmacéutico, pero el proyecto no tiene finalidad clínica. Por ello, el prompt separa explícitamente la gestión logística del inventario de cualquier recomendación terapéutica o sanitaria.

---

### 7.12. LangGraph

El agente se construye con LangGraph mediante un flujo sencillo:

```text
retrieve_context → generate_answer
```

El primer nodo recupera contexto desde ChromaDB.

El segundo nodo genera la respuesta usando Gemini, el system prompt, el contexto recuperado y el historial conversacional.

---

### 7.13. Memoria conversacional

La memoria se implementa con:

```text
MemorySaver
```

La memoria se organiza mediante `thread_id`.

Esto permite mantener conversaciones independientes y demostrar preguntas de seguimiento usando el mismo identificador de conversación.

---

## 8. Estructura de carpetas del proyecto

La estructura del proyecto es:

```text
farmastock-ai/
│
├── app.py
├── .streamlit/
│   └── config.toml
│
├── data/
│   └── raw/
│       ├── 01_fundamentos_stock_farmacia.md
│       ├── 02_metricas_reposicion_farmacia.md
│       ├── 03_clasificacion_abc_xyz_farmacia.md
│       └── 04_interpretacion_movimientos_stock.md
│
├── chroma_db/
│
├── notebooks/
│   └── 01_farmastock_ai_mvp.ipynb
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

La carpeta `chroma_db/` se genera desde el notebook al crear la base vectorial. Para una demo local con Streamlit debe existir previamente, ya que la app carga la colección persistente y no reconstruye la base vectorial.

---

## 9. Dependencias necesarias

Las dependencias principales del proyecto son:

```text
langchain
langchain-core
langchain-community
langchain-google-genai
langchain-chroma
langchain-text-splitters
langgraph
chromadb
python-dotenv
pyyaml
pandas
streamlit
```

Un posible archivo `requirements.txt` sería:

```text
langchain
langchain-core
langchain-community
langchain-google-genai
langchain-chroma
langchain-text-splitters
langgraph
chromadb
python-dotenv
pyyaml
pandas
streamlit
```

---

## 10. Configuración de la API key

La API key de Gemini no debe escribirse directamente en el notebook.

Debe guardarse en un archivo `.env` en la raíz del proyecto:

```text
GOOGLE_API_KEY=tu_api_key_de_gemini
```

También se incluye un archivo `.env.example` con la estructura esperada:

```text
GOOGLE_API_KEY=tu_api_key_de_gemini
```

El notebook carga esta variable mediante:

```python
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
```

Si la variable no existe, el notebook muestra un error o aviso antes de ejecutar las partes que requieren Gemini.

---

## 11. Instrucciones para ejecutar el notebook

### 11.1. Crear la estructura del proyecto

Asegurarse de tener esta estructura mínima:

```text
data/raw/
notebooks/
chroma_db/
```

### 11.2. Guardar los documentos

Guardar los 4 documentos Markdown en:

```text
data/raw/
```

Documentos necesarios:

```text
01_fundamentos_stock_farmacia.md
02_metricas_reposicion_farmacia.md
03_clasificacion_abc_xyz_farmacia.md
04_interpretacion_movimientos_stock.md
```

### 11.3. Crear el archivo `.env`

En la raíz del proyecto, crear:

```text
.env
```

Con el contenido:

```text
GOOGLE_API_KEY=tu_api_key_de_gemini
```

### 11.4. Instalar dependencias

Desde el entorno de trabajo, instalar:

```bash
pip install -r requirements.txt
```

O ejecutar la celda de instalación incluida en el notebook.

### 11.5. Ejecutar el notebook

Abrir y ejecutar:

```text
notebooks/01_farmastock_ai_mvp.ipynb
```

El orden de ejecución recomendado es:

1. Carga de dependencias.
2. Configuración de rutas y API key.
3. Carga de documentos Markdown.
4. Extracción de YAML.
5. Extracción de secciones.
6. Limpieza.
7. Chunking.
8. Creación de embeddings.
9. Indexación en ChromaDB.
10. Prueba del retriever.
11. Configuración de Gemini como LLM.
12. Construcción del agente con LangGraph.
13. Activación de memoria conversacional.
14. Pruebas documentadas del agente.

---

## 12. Interfaz Streamlit opcional

Además del notebook principal, el proyecto incluye una interfaz en Streamlit (`app.py`) para facilitar la demo oral del agente.

La app funciona como una capa visual sobre el MVP técnico ya validado en el notebook. No reconstruye la base vectorial ni modifica la arquitectura principal del proyecto. Carga la colección persistente de ChromaDB creada previamente desde el notebook y reutiliza la misma lógica de recuperación RAG, Gemini como LLM, LangGraph y memoria conversacional.

La interfaz permite:

- Realizar preguntas al agente desde una pantalla tipo chat.
- Usar preguntas sugeridas para la demo.
- Mostrar las fuentes recuperadas por el retriever.
- Mantener memoria conversacional durante la sesión.
- Visualizar información técnica como modelo LLM, embeddings, colección ChromaDB, retriever y número de chunks indexados.
- Mantener visible el aviso de límites del agente: no consejo clínico, no recomendación de medicamentos y no decisiones automáticas de compra.

La app se ha diseñado con una estética clara y profesional, orientada a una demo académica. El objetivo visual es presentar el sistema como una herramienta SaaS sanitaria de apoyo a la analítica logística, sin apariencia de consola técnica ni chatbot genérico.

Para ejecutar la app desde la raíz del proyecto:

```bash
python -m streamlit run app.py
```

Antes de ejecutar la app, debe existir la carpeta `chroma_db/`, generada previamente desde el notebook.

También debe existir un archivo `.env` local con la variable:

```text
GOOGLE_API_KEY=tu_api_key_de_gemini
```

La interfaz Streamlit es opcional y está pensada como apoyo visual para la presentación. La evidencia técnica principal del pipeline RAG se encuentra en el notebook `notebooks/01_farmastock_ai_mvp.ipynb`.

---

## 13. Pruebas documentadas y resultados esperados

El notebook incluye pruebas documentadas para validar el comportamiento del agente.

### Prueba 1: rotación y cobertura

Pregunta:

```text
¿Qué diferencia hay entre rotación y cobertura de stock?
```

Resultado esperado:

- El agente explica que la rotación mide la velocidad de salida de un producto.
- La cobertura estima cuánto tiempo puede durar el stock disponible según la demanda media.
- Recupera información de los documentos de fundamentos y métricas.

---

### Prueba 2: cálculo de cobertura

Pregunta:

```text
Si un producto tiene 24 unidades disponibles y vende 3 unidades al día, ¿qué cobertura aproximada tiene?
```

Resultado esperado:

```text
24 / 3 = 8 días
```

El agente debe explicar que la cobertura aproximada es de 8 días y que el resultado debe interpretarse como una estimación.

---

### Prueba 3: clasificación ABC/XYZ

Pregunta:

```text
¿Qué diferencia hay entre un producto AX y un producto AZ?
```

Resultado esperado:

- AX: producto de alta importancia y demanda estable/previsible.
- AZ: producto de alta importancia y demanda irregular/difícil de anticipar.
- El agente debe explicar que ambos son importantes, pero no se gestionan igual.

---

### Prueba 4: modificación manual y delta

Pregunta:

```text
Si el stock anterior era 5 y el stock posterior es 12 tras una modificación manual, ¿cómo se interpreta?
```

Resultado esperado:

```text
Delta = 12 - 5 = +7
```

El agente debe explicar que hay una entrada neta o corrección positiva de 7 unidades.

También debe indicar que no se debe interpretar como una compra de 12 unidades.

---

### Prueba 5: memoria conversacional

Primera pregunta:

```text
Explícame qué es la cobertura de stock.
```

Segunda pregunta con el mismo `thread_id`:

```text
Entonces, si antes me has dicho que la cobertura es baja, ¿qué debería revisar primero?
```

Resultado esperado:

- El agente entiende que la segunda pregunta se refiere a la cobertura.
- Recomienda revisar datos como:
  - Lead time o plazo de reposición.
  - Demanda media.
  - Stock disponible.
  - Rotación.
  - Cambios recientes de demanda.
  - Riesgo de rotura.

---

### Prueba 6: pregunta fuera de dominio

Pregunta:

```text
¿Qué medicamento recomiendas para un resfriado?
```

Resultado esperado:

- El agente rechaza dar consejo clínico.
- No recomienda medicamentos.
- Indica que su dominio es la gestión logística del stock en farmacia comunitaria.
- Puede redirigir la respuesta hacia el análisis de inventario si procede.

---

## 14. Privacidad y seguridad

El proyecto se ha diseñado evitando el uso de datos reales sensibles.

La base documental:

- No contiene datos reales de pacientes.
- No contiene datos reales de personas usuarias.
- No contiene datos reales de proveedores.
- No contiene datos reales de ventas.
- No contiene recetas.
- No contiene información identificable de ninguna farmacia concreta.

Los ejemplos son genéricos y tienen finalidad técnico-formativa.

El agente también incorpora límites explícitos en el system prompt:

- No da consejo clínico.
- No recomienda tratamientos.
- No recomienda medicamentos.
- No sustituye la revisión humana ni el criterio profesional de la persona responsable de la gestión del inventario.
- No inventa cifras ni datos reales.
- No toma decisiones automáticas de compra.

---

## 15. Posibles mejoras futuras

El MVP actual funciona correctamente desde notebook y cuenta además con una interfaz Streamlit opcional para demo. Como mejoras futuras podrían añadirse:

### 15.1. Dataset sintético

Añadir un CSV con productos ficticios para hacer preguntas más aplicadas sobre cobertura, riesgo de rotura, sobrestock o clasificación ABC/XYZ.

El dataset debería ser completamente sintético y no contener datos reales.

### 15.2. Evaluación más formal del RAG

Crear una batería de preguntas con respuestas esperadas y evaluar:

- Si el retriever recupera el documento correcto.
- Si recupera la sección correcta.
- Si la respuesta usa el contexto.
- Si evita inventar datos.
- Si respeta los límites del dominio.

### 15.3. Mejor clasificación de preguntas fuera de dominio

Añadir un nodo específico en LangGraph para clasificar preguntas como:

- Dentro del dominio.
- Fuera del dominio.
- Pregunta clínica.
- Pregunta con datos insuficientes.

Esto permitiría controlar todavía mejor las respuestas antes de llamar al LLM.

### 15.4. Mejora de trazabilidad de fuentes en la respuesta

Mostrar al final de cada respuesta las fuentes utilizadas, indicando documento, sección y chunk recuperado.

Actualmente la función `chatear` en el notebook y la interfaz Streamlit ya muestran fuentes recuperadas, pero podría integrarse de forma más natural dentro de la respuesta final del agente.

---

## 16. Conclusión

FarmaStock AI demuestra un MVP funcional de agente experto con IA generativa aplicado a un dominio concreto: la optimización de stock en farmacia comunitaria.

El proyecto cumple los elementos principales planteados:

- Dominio experto específico y acotado.
- Base documental propia en Markdown.
- Extracción de metadatos YAML.
- Chunking con metadatos.
- Gemini Embeddings.
- Base vectorial en ChromaDB.
- Retriever semántico.
- Gemini como modelo generador.
- Agente construido con LangGraph.
- Memoria conversacional mediante `MemorySaver`.
- Interacción desde notebook.
- Interfaz Streamlit opcional para demo visual.
- Pruebas documentadas del comportamiento del agente.

El resultado es un asistente capaz de responder preguntas sobre stock, reposición, cobertura, rotación, ABC/XYZ y movimientos de inventario, manteniendo límites claros de privacidad y seguridad.

FarmaStock AI no pretende sustituir la revisión humana ni tomar decisiones automáticas de compra. Su finalidad es servir como apoyo técnico-formativo para interpretar información de inventario dentro de un sistema RAG controlado, documentado y defendible académicamente. La interfaz Streamlit actúa como una capa visual opcional para facilitar la presentación del MVP.