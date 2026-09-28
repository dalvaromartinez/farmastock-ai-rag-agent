# FarmaStock Knowledge Assistant

> RAG-based knowledge assistant for pharmacy stock-management concepts.

**FarmaStock Knowledge Assistant** es un proyecto de portfolio de IA generativa orientado a la gestión logística de stock en farmacia comunitaria.

El sistema utiliza una base documental propia, recuperación semántica con ChromaDB, Gemini para embeddings y generación, un workflow de dos nodos construido con LangGraph y una interfaz Streamlit.

El objetivo del proyecto es demostrar de forma práctica:

- procesamiento documental;
- chunking con metadatos;
- embeddings;
- vector stores;
- retrieval semántico;
- Retrieval-Augmented Generation (RAG);
- orquestación con LangGraph;
- memoria conversacional temporal;
- trazabilidad de las fuentes recuperadas;
- construcción de una interfaz de demostración con Streamlit.

El sistema **no es un agente autónomo**. El flujo es determinista y está formado por dos nodos principales: recuperación de contexto y generación de respuesta.

---

## 1. Dominio

El dominio del proyecto es:

> **Optimización de stock en farmacia comunitaria**

El asistente está orientado a conceptos logísticos y formativos relacionados con:

- rotación;
- cobertura;
- stock mínimo;
- stock máximo;
- stock de seguridad;
- punto de pedido;
- demanda histórica;
- lead time;
- riesgo de rotura;
- sobrestock;
- clasificación ABC/XYZ;
- interpretación de movimientos de inventario.

No proporciona consejo clínico, no recomienda medicamentos ni tratamientos y no toma decisiones automáticas de compra.

---

## 2. Base documental

La base de conocimiento está formada por cuatro documentos Markdown propios creados para este proyecto:

```text
data/raw/01_fundamentos_stock_farmacia.md
data/raw/02_metricas_reposicion_farmacia.md
data/raw/03_clasificacion_abc_xyz_farmacia.md
data/raw/04_interpretacion_movimientos_stock.md
```

Los documentos contienen ejemplos genéricos y material técnico-formativo.

No contienen datos reales de pacientes, personas usuarias, proveedores, ventas, recetas ni farmacias concretas.

Cada documento incluye front matter YAML con metadatos como:

```yaml
title: "..."
document_id: "..."
version: "1.0"
domain: "Optimización de stock en farmacia comunitaria"
use_in_rag: true
contains_real_data: false
```

`use_in_rag` controla si un documento puede incorporarse al índice vectorial.

---

## 3. Procesamiento documental

El pipeline de indexación sigue este flujo:

```text
Markdown
   ↓
front matter YAML
   ↓
filtrado por use_in_rag
   ↓
secciones Markdown ##
   ↓
exclusión de secciones de preguntas
   ↓
limpieza básica
   ↓
chunking
   ↓
Gemini Embeddings
   ↓
ChromaDB
```

### Segmentación por secciones

Antes del chunking por tamaño, los documentos se dividen utilizando encabezados Markdown de nivel 2:

```text
##
```

Las secciones tituladas como:

```text
Preguntas que puede responder este documento
```

se conservan en los archivos originales pero se excluyen del índice.

Con el corpus actual se obtienen **41 secciones indexables**:

| Documento | Secciones indexables |
|---|---:|
| Fundamentos de stock | 9 |
| Métricas y reposición | 10 |
| Clasificación ABC/XYZ | 10 |
| Movimientos de stock | 12 |
| **Total** | **41** |

### Chunking

El splitter utilizado es:

```text
RecursiveCharacterTextSplitter
```

con:

```text
chunk_size = 1000
chunk_overlap = 150
```

Cada sección recibe además contexto documental antes de dividirse:

```text
Documento: <título>
Sección: <sección>
```

Cada chunk conserva metadatos de trazabilidad como:

- `document_id`;
- `filename`;
- `section_number`;
- `section_title`;
- `chunk_index`;
- `chunk_id`;
- `domain`;
- `contains_real_data`;
- `use_in_rag`.

Con el corpus actual y esta configuración se generan **118 chunks**:

```text
01_fundamentos_stock_farmacia       27
02_metricas_reposicion_farmacia     27
03_clasificacion_abc_xyz_farmacia   29
04_interpretacion_movimientos_stock  35
---------------------------------------
Total                              118
```

La integridad del índice no se valida únicamente contra el número 118. `build_index.py` compara dinámicamente los registros persistidos en ChromaDB con `len(chunks)` y aborta si no coinciden.

---

## 4. Embeddings y vector store

Los embeddings se generan mediante:

```text
models/gemini-embedding-001
```

La base vectorial se implementa con ChromaDB.

Colección:

```text
farmastock_ai_docs
```

Persistencia local:

```text
chroma_db/
```

`chroma_db/` no se versiona en Git y debe construirse localmente mediante:

```bash
python build_index.py
```

El builder reconstruye el índice desde cero.

Si existe una ChromaDB anterior y no puede eliminarse correctamente, el proceso se detiene para evitar duplicar documentos o trabajar sobre un índice parcialmente reconstruido.

---

## 5. Retrieval

La recuperación utiliza similitud semántica:

```text
search_type = "similarity"
k = 4
```

Para cada pregunta se recuperan los cuatro chunks más similares.

Actualmente el sistema **no implementa**:

- similarity threshold;
- reranking;
- hybrid search;
- contextual retrieval;
- query rewriting basado en la conversación.

El retriever recibe únicamente la pregunta actual.

---

## 6. RAG y Gemini

Los chunks recuperados se formatean como contexto incluyendo:

```text
Documento
Sección
Chunk ID
Contenido
```

Ese contexto, junto con el system prompt, el historial conversacional reciente y la pregunta actual, se envía a:

```text
gemini-2.5-flash
```

con:

```text
temperature = 0.2
```

El prompt establece límites explícitos:

- utilizar el contexto recuperado como fuente principal;
- reconocer cuando la información disponible no es suficiente;
- no inventar cifras;
- no dar consejo clínico;
- no recomendar tratamientos o medicamentos;
- no tomar decisiones automáticas de compra.

---

## 7. LangGraph

LangGraph organiza el workflow RAG.

El grafo tiene dos nodos:

```text
START
  ↓
retrieve_context
  ↓
generate_answer
  ↓
END
```

### `retrieve_context`

Recibe la pregunta actual y ejecuta el retriever de ChromaDB.

Produce:

- `retrieved_docs`;
- `context`.

### `generate_answer`

Utiliza:

- system prompt;
- contexto recuperado;
- historial conversacional reciente;
- pregunta actual.

Después llama a Gemini y actualiza el historial.

Este diseño utiliza LangGraph como mecanismo de orquestación y checkpointing. No implementa planificación autónoma, selección dinámica de herramientas, loops de razonamiento ni decisiones agentic.

---

## 8. Memoria conversacional

La memoria se implementa mediante:

```text
MemorySaver
```

y se organiza por:

```text
thread_id
```

Cuando se reutiliza el mismo `thread_id`, el workflow puede recuperar el historial conversacional guardado en memoria y utilizarlo en la generación de la siguiente respuesta.

### Qué persiste

El historial puede mantenerse mientras siga vivo el proceso que contiene el `MemorySaver`.

### Qué no persiste

La conversación no se almacena en:

- ChromaDB;
- archivos;
- SQLite;
- una base de datos externa;
- un servicio de persistencia.

Al reiniciar el proceso, esa memoria se pierde.

Además, la memoria conversacional **no se utiliza para reformular la búsqueda**.

El retrieval actual ejecuta:

```text
retriever.invoke(question)
```

sobre la pregunta actual.

El historial se incorpora después, durante la generación de la respuesta.

---

## 9. Fuentes recuperadas

Tanto el notebook como Streamlit pueden mostrar los metadatos de los chunks recuperados:

- documento;
- sección;
- `chunk_id`.

Estas referencias representan **fuentes recuperadas por el retriever**.

No deben interpretarse como una atribución automática de cada frase generada por el LLM a un chunk específico.

---

## 10. Streamlit

`app.py` implementa la interfaz visual del proyecto.

Permite:

- realizar preguntas en formato chat;
- utilizar preguntas sugeridas;
- visualizar las fuentes recuperadas;
- mantener una conversación temporal mediante `thread_id`;
- consultar la configuración del modelo y del retriever;
- comprobar el número de chunks presentes en ChromaDB;
- revisar los documentos esperados.

La aplicación utiliza el índice persistente construido previamente por `build_index.py`.

No reconstruye la base vectorial por sí sola.

---

## 11. Estructura del repositorio

```text
farmastock-ai-rag-agent/
│
├── app.py
├── build_index.py
├── README.md
├── LICENSE
├── requirements.txt
├── .env.example
├── .gitignore
│
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
└── notebooks/
    └── 01_farmastock_ai_mvp.ipynb
```

Durante la ejecución se genera además:

```text
chroma_db/
```

Este directorio es local y está excluido mediante `.gitignore`.

---

## 12. Puesta en marcha

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd farmastock-ai-rag-agent
```

### 2. Crear un entorno virtual

```bash
python -m venv .venv
```

Activar el entorno según el sistema operativo.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Gemini

Crear un archivo:

```text
.env
```

a partir de:

```text
.env.example
```

y definir:

```text
GOOGLE_API_KEY=tu_api_key_de_gemini
```

El proyecto no incluye ninguna API key real.

### 5. Construir el índice

```bash
python build_index.py
```

El script:

1. carga los cuatro documentos;
2. valida el front matter;
3. aplica `use_in_rag`;
4. extrae las secciones;
5. aplica limpieza;
6. genera los chunks;
7. crea embeddings;
8. reconstruye ChromaDB;
9. valida que el número persistido coincida con los chunks generados.

Con el corpus actual se esperan 118 chunks.

### 6. Ejecutar Streamlit

```bash
python -m streamlit run app.py
```

---

## 13. Notebook

El notebook:

```text
notebooks/01_farmastock_ai_mvp.ipynb
```

se conserva como artefacto de:

- experimentación;
- explicación técnica;
- inspección del pipeline;
- demostraciones de retrieval;
- evaluación cualitativa.

Ya no es un requisito para arrancar la aplicación.

La creación reproducible del índice corresponde a:

```text
build_index.py
```

---

## 14. Evaluación

El proyecto separa dos tipos de comprobación.

### Retrieval checks

Se plantea una batería mínima de cuatro comprobaciones reproducibles.

Cada consulta define un `document_id` esperado y verifica que aparezca dentro del top-4 recuperado.

Estas comprobaciones evalúan únicamente la recuperación documental.

### Manual qualitative evaluation

El notebook contiene seis escenarios generativos:

1. diferencia entre rotación y cobertura;
2. cálculo sencillo de cobertura;
3. clasificación AX frente a AZ;
4. interpretación de modificación manual y delta;
5. seguimiento conversacional;
6. pregunta clínica fuera de dominio.

Estos escenarios son:

> **manual qualitative evaluation**

No son tests automatizados, no generan una métrica de accuracy y no deben presentarse como una evaluación cuantitativa del sistema.

---

## 15. Limitaciones técnicas actuales

El MVP utiliza un diseño deliberadamente sencillo.

No incorpora:

- reranker;
- similarity threshold;
- hybrid search;
- contextual retrieval;
- query rewriting;
- memoria persistente;
- router de intención;
- clasificación determinista de preguntas fuera de dominio;
- herramientas externas;
- comportamiento autónomo.

Estas limitaciones se documentan para diferenciar claramente las capacidades implementadas de posibles extensiones futuras.

---

## 16. Privacidad y seguridad

El repositorio no versiona:

```text
.env
chroma_db/
.venv/
```

La base documental declara:

```yaml
contains_real_data: false
```

y está formada por contenido técnico-formativo creado para el proyecto.

No se incluyen datos reales sensibles ni identificables de pacientes, personas usuarias, proveedores o farmacias.

La interfaz no muestra deliberadamente tracebacks internos al visitante.

---

## 17. Dependencias

El proyecto utiliza principalmente:

### Runtime

```text
langchain-core
langchain-google-genai
langchain-chroma
langchain-text-splitters
langgraph
chromadb
python-dotenv
pyyaml
streamlit
```

### Notebook / desarrollo

```text
ipykernel
jupyter
```

El archivo `requirements.txt` todavía no fija versiones.

Las versiones se congelarán después de completar una ejecución limpia end-to-end en un entorno reproducible.

---

## 18. Licencia

Este proyecto se distribuye bajo licencia MIT.

Consulta `LICENSE` para más información.
