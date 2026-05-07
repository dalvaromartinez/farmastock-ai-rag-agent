import os
import uuid
from pathlib import Path
from typing import TypedDict, List, Dict, Any, Optional

import streamlit as st
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


# ============================================================
# Configuración general
# ============================================================

PROJECT_NAME = "FarmaStock AI"
PROJECT_DOMAIN = "Optimización de stock en farmacia comunitaria"

COLLECTION_NAME = "farmastock_ai_docs"
EMBEDDING_MODEL = "models/gemini-embedding-001"
GEMINI_LLM_MODEL = "gemini-2.5-flash"

RETRIEVER_K = 4
TEMPERATURE = 0.2


# ============================================================
# Rutas
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"
DATA_DIR = BASE_DIR / "data" / "raw"


# ============================================================
# System prompt
# ============================================================

SYSTEM_PROMPT = """
Eres FarmaStock AI, un asistente experto en análisis y optimización de stock en farmacia comunitaria.

Tu dominio está limitado a la gestión logística del inventario en farmacia comunitaria. Puedes responder preguntas sobre rotación, cobertura, stock mínimo, stock máximo, stock de seguridad, punto de pedido, demanda histórica, lead time, sobrestock, roturas, clasificación ABC/XYZ e interpretación de movimientos de inventario.

Debes basar tus respuestas principalmente en el contexto recuperado desde la base de conocimiento vectorial de ChromaDB. Si el contexto recuperado no contiene información suficiente para responder con seguridad, dilo claramente y explica qué dato o documento faltaría.

No debes dar consejo clínico, recomendar tratamientos, recomendar medicamentos ni sustituir la revisión humana ni el criterio profesional de la persona responsable de la gestión del inventario. Si la pregunta pide consejo clínico o recomendación terapéutica, indica que está fuera de tu dominio y redirige la respuesta al ámbito de gestión de stock si procede.

No inventes cifras de ventas, stock, demanda, márgenes, proveedores ni datos reales de una farmacia concreta. Si hacen falta datos numéricos y no están disponibles, explica la fórmula general o pide los datos necesarios.

No utilices datos reales sensibles ni hagas referencia a personas usuarias concretas, proveedores concretos o farmacias reales.

Responde siempre en español, con tono claro, profesional y práctico. Prioriza respuestas útiles, estructadas y fáciles de entender. Incluye límites o advertencias solo cuando sean relevantes para la pregunta.
""".strip()


# ============================================================
# Estado LangGraph
# ============================================================

class FarmaStockState(TypedDict):
    question: str
    chat_history: List[Dict[str, str]]
    retrieved_docs: List[Document]
    context: str
    answer: str


# ============================================================
# Utilidades RAG
# ============================================================

def format_docs(docs: List[Document]) -> str:
    """
    Formatea los documentos recuperados para insertarlos como contexto.
    Incluye documento, sección y chunk_id para trazabilidad.
    """
    formatted_parts = []

    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata

        document_id = metadata.get("document_id", "documento_desconocido")
        section_title = metadata.get("section_title", "sección_desconocida")
        chunk_id = metadata.get("chunk_id", "chunk_desconocido")

        formatted_parts.append(
            f"[Fuente {i}]\n"
            f"Documento: {document_id}\n"
            f"Sección: {section_title}\n"
            f"Chunk ID: {chunk_id}\n\n"
            f"{doc.page_content}"
        )

    return ("\n\n" + "-" * 80 + "\n\n").join(formatted_parts)


def build_chat_history_text(chat_history: List[Dict[str, str]], max_turns: int = 6) -> str:
    """
    Convierte el historial conversacional en texto.
    Limita el número de turnos para evitar prompts demasiado largos.
    """
    if not chat_history:
        return "No hay historial previo relevante."

    recent_history = chat_history[-max_turns:]
    lines = []

    for turn in recent_history:
        role = turn.get("role", "unknown")
        content = turn.get("content", "")

        if role == "user":
            lines.append(f"Usuario: {content}")
        elif role == "assistant":
            lines.append(f"Asistente: {content}")
        else:
            lines.append(f"{role}: {content}")

    return "\n".join(lines)


# ============================================================
# Carga de componentes
# ============================================================

@st.cache_resource
def load_components():
    """
    Carga embeddings, ChromaDB, retriever y LLM.

    Importante:
    - No reconstruye la base vectorial.
    - Usa la colección persistente creada previamente desde el notebook.
    """
    load_dotenv()

    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not google_api_key:
        raise ValueError(
            "No se ha encontrado GOOGLE_API_KEY. "
            "Crea un archivo .env en la raíz del proyecto con GOOGLE_API_KEY=tu_clave."
        )

    if not CHROMA_DIR.exists():
        raise FileNotFoundError(
            f"No se ha encontrado la carpeta ChromaDB en: {CHROMA_DIR}. "
            "Ejecuta primero el notebook para crear la base vectorial."
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=google_api_key,
    )

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVER_K},
    )

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_LLM_MODEL,
        google_api_key=google_api_key,
        temperature=TEMPERATURE,
    )

    return vectorstore, retriever, llm


# ============================================================
# Construcción del grafo LangGraph
# ============================================================

def build_graph(retriever, llm):
    """
    Construye el agente RAG con LangGraph.
    Flujo:
    START -> retrieve_context -> generate_answer -> END
    """

    def retrieve_context(state: FarmaStockState) -> Dict[str, Any]:
        question = state["question"]
        docs = retriever.invoke(question)
        context = format_docs(docs)

        return {
            "retrieved_docs": docs,
            "context": context,
        }

    def generate_answer(state: FarmaStockState) -> Dict[str, Any]:
        question = state["question"]
        context = state.get("context", "")
        chat_history = state.get("chat_history", [])

        chat_history_text = build_chat_history_text(chat_history)

        user_prompt = f"""
Contexto recuperado desde la base de conocimiento:
{context}

Historial conversacional reciente:
{chat_history_text}

Pregunta actual del usuario:
{question}

Instrucciones para responder:
- Usa el contexto recuperado como fuente principal.
- Si el contexto no es suficiente, dilo claramente.
- No inventes datos ni cifras.
- No des consejo clínico ni recomiendes tratamientos.
- Responde de forma clara, práctica y en español.
""".strip()

        response = llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_prompt),
            ]
        )

        answer = response.content

        updated_history = chat_history + [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]

        return {
            "answer": answer,
            "chat_history": updated_history,
        }

    builder = StateGraph(FarmaStockState)

    builder.add_node("retrieve_context", retrieve_context)
    builder.add_node("generate_answer", generate_answer)

    builder.add_edge(START, "retrieve_context")
    builder.add_edge("retrieve_context", "generate_answer")
    builder.add_edge("generate_answer", END)

    memory = MemorySaver()
    app = builder.compile(checkpointer=memory)

    return app


@st.cache_resource
def load_agent():
    """
    Carga los componentes y construye el agente.
    """
    vectorstore, retriever, llm = load_components()
    app = build_graph(retriever, llm)
    return app, vectorstore


# ============================================================
# Función de chat para Streamlit
# ============================================================

def run_agent(app, mensaje: str, thread_id: str = "streamlit_demo") -> Dict[str, Any]:
    """
    Ejecuta el agente con memoria conversacional por thread_id.
    Recupera el historial previo del estado de LangGraph.
    """
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    try:
        previous_state = app.get_state(config)
        previous_values = previous_state.values if previous_state and previous_state.values else {}
        previous_history = previous_values.get("chat_history", [])
    except Exception:
        previous_history = []

    initial_state = {
        "question": mensaje,
        "chat_history": previous_history,
        "retrieved_docs": [],
        "context": "",
        "answer": "",
    }

    result = app.invoke(initial_state, config=config)

    return result


# ============================================================
# Estilos visuales
# ============================================================

def inject_custom_css():
    st.markdown(
        """
        <style>
        :root {
            --fs-bg: #F7F4EF;
            --fs-bg-secondary: #EDE7DC;
            --fs-card: #FFFCF7;
            --fs-text: #171717;
            --fs-muted: #6F6A63;
            --fs-green: #2E7D5B;
            --fs-green-dark: #245E46;
            --fs-green-soft: #EAF4EF;
            --fs-gold: #B89B5E;
            --fs-border: #D8D0C3;
            --fs-shadow: rgba(23, 23, 23, 0.07);
        }

        html, body, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 10% 10%, rgba(46,125,91,0.08), transparent 28%),
                radial-gradient(circle at 88% 8%, rgba(184,155,94,0.12), transparent 24%),
                linear-gradient(180deg, #F7F4EF 0%, #F3EFE7 100%) !important;
            color: var(--fs-text) !important;
        }

        [data-testid="stHeader"] {
            background: rgba(247, 244, 239, 0.82) !important;
            backdrop-filter: blur(10px);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #EDE7DC 0%, #E6DFD2 100%) !important;
            border-right: 1px solid var(--fs-border);
        }

        [data-testid="stSidebar"] * {
            color: var(--fs-text);
        }

        .block-container {
            max-width: 1320px;
            padding-top: 2.2rem;
            padding-bottom: 3.5rem;
        }

        .fs-hero {
            position: relative;
            overflow: hidden;
            background:
                linear-gradient(135deg, rgba(255,252,247,0.98) 0%, rgba(234,244,239,0.92) 100%);
            border: 1px solid var(--fs-border);
            border-radius: 30px;
            padding: 2.1rem 2.25rem;
            box-shadow: 0 24px 70px rgba(23, 23, 23, 0.07);
            margin-bottom: 1.1rem;
        }

        .fs-hero::before {
            content: "";
            position: absolute;
            width: 420px;
            height: 420px;
            right: -160px;
            top: -180px;
            background: radial-gradient(circle, rgba(46,125,91,0.14), transparent 64%);
            pointer-events: none;
        }

        .fs-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.38rem 0.75rem;
            border-radius: 999px;
            background: rgba(46, 125, 91, 0.10);
            color: var(--fs-green-dark);
            border: 1px solid rgba(46, 125, 91, 0.22);
            font-weight: 800;
            font-size: 0.78rem;
            margin-bottom: 1.05rem;
            letter-spacing: 0.01em;
        }

        .fs-title {
            font-size: 3.4rem;
            line-height: 1.02;
            font-weight: 900;
            letter-spacing: -0.07em;
            color: var(--fs-text);
            margin: 0;
        }

        .fs-subtitle {
            font-size: 1.08rem;
            line-height: 1.7;
            color: var(--fs-muted);
            margin-top: 0.95rem;
            max-width: 820px;
        }

        .fs-badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1.25rem;
        }

        .fs-badge {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.48rem 0.78rem;
            font-size: 0.78rem;
            font-weight: 800;
            background: rgba(255, 252, 247, 0.86);
            color: var(--fs-muted);
            border: 1px solid var(--fs-border);
        }

        .fs-limit-banner {
            background: rgba(234, 244, 239, 0.92);
            border: 1px solid rgba(46, 125, 91, 0.24);
            color: #235B43;
            border-radius: 20px;
            padding: 0.95rem 1.08rem;
            margin: 1rem 0 1.25rem 0;
            font-size: 0.94rem;
            line-height: 1.55;
            box-shadow: 0 12px 28px rgba(46, 125, 91, 0.06);
        }

        .fs-card-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin: 1.2rem 0 1.7rem 0;
        }

        .fs-card {
            background: rgba(255, 252, 247, 0.94);
            border: 1px solid var(--fs-border);
            border-radius: 24px;
            padding: 1.18rem 1.22rem;
            box-shadow: 0 18px 42px rgba(23, 23, 23, 0.055);
        }

        .fs-card-icon {
            width: 40px;
            height: 40px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 14px;
            background: var(--fs-green-soft);
            color: var(--fs-green);
            font-size: 1.22rem;
            margin-bottom: 0.82rem;
        }

        .fs-card-title {
            font-weight: 850;
            color: var(--fs-text);
            font-size: 1rem;
            margin-bottom: 0.32rem;
        }

        .fs-card-text {
            color: var(--fs-muted);
            font-size: 0.9rem;
            line-height: 1.52;
        }

        .fs-section-title {
            color: var(--fs-text);
            font-size: 1.45rem;
            font-weight: 900;
            letter-spacing: -0.045em;
            margin: 0.3rem 0 0.35rem 0;
        }

        .fs-section-subtitle {
            color: var(--fs-muted);
            font-size: 0.94rem;
            margin-bottom: 0.95rem;
            line-height: 1.55;
        }

        .fs-divider {
            height: 1px;
            background: var(--fs-border);
            margin: 1.6rem 0;
        }

        .fs-panel-static {
            background: rgba(255, 252, 247, 0.9);
            border: 1px solid var(--fs-border);
            border-radius: 24px;
            padding: 1.1rem 1.15rem;
            box-shadow: 0 18px 44px rgba(23, 23, 23, 0.052);
            margin-bottom: 0.9rem;
        }

        .fs-panel-title {
            font-size: 0.95rem;
            font-weight: 850;
            color: var(--fs-text);
            margin-bottom: 0.25rem;
        }

        .fs-panel-caption {
            font-size: 0.84rem;
            color: var(--fs-muted);
            line-height: 1.45;
        }

        .fs-pill {
            display: inline-flex;
            align-items: center;
            max-width: 100%;
            padding: 0.34rem 0.58rem;
            border-radius: 999px;
            border: 1px solid rgba(46, 125, 91, 0.22);
            background: rgba(234, 244, 239, 0.8);
            color: var(--fs-green-dark);
            font-size: 0.78rem;
            font-weight: 800;
            margin: 0.18rem 0.16rem 0.18rem 0;
            word-break: break-word;
        }

        .fs-sidebar-label {
            font-size: 0.72rem;
            color: var(--fs-muted);
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-top: 0.7rem;
            margin-bottom: 0.2rem;
        }

        .fs-sidebar-value {
            background: rgba(255, 252, 247, 0.72);
            border: 1px solid var(--fs-border);
            border-radius: 14px;
            padding: 0.52rem 0.62rem;
            color: var(--fs-text);
            font-size: 0.82rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            overflow-wrap: anywhere;
            margin-bottom: 0.55rem;
        }

        .fs-doc-item {
            background: rgba(234, 244, 239, 0.78);
            border: 1px solid rgba(46, 125, 91, 0.16);
            border-radius: 14px;
            padding: 0.55rem 0.62rem;
            margin-bottom: 0.45rem;
            font-size: 0.78rem;
            font-weight: 750;
            color: var(--fs-green-dark);
            overflow-wrap: anywhere;
        }

        .fs-doc-missing {
            background: rgba(255, 240, 235, 0.9);
            border: 1px solid rgba(185, 79, 62, 0.22);
            color: #8A3327;
        }

        .fs-chat-label {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.76rem;
            font-weight: 900;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--fs-muted);
            margin-bottom: 0.45rem;
        }

        .fs-chat-box {
            border-radius: 24px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.85rem;
            box-shadow: 0 14px 36px rgba(23, 23, 23, 0.046);
        }

        .fs-chat-user {
            background: rgba(255, 252, 247, 0.96);
            border: 1px solid rgba(184, 155, 94, 0.38);
        }

        .fs-chat-assistant {
            background: rgba(255, 252, 247, 0.98);
            border: 1px solid rgba(46, 125, 91, 0.22);
        }

        .fs-empty-chat {
            border: 1px dashed var(--fs-border);
            background: rgba(255, 252, 247, 0.58);
            border-radius: 24px;
            padding: 1.2rem;
            color: var(--fs-muted);
            font-size: 0.95rem;
            line-height: 1.55;
        }

        .fs-source-card {
            background: #FFFFFF;
            border: 1px solid var(--fs-border);
            border-radius: 16px;
            padding: 0.85rem 0.9rem;
            margin-bottom: 0.7rem;
        }

        .fs-source-card strong {
            color: var(--fs-green);
        }

        .fs-small-muted {
            color: var(--fs-muted);
            font-size: 0.84rem;
        }

        .fs-footer {
            color: var(--fs-muted);
            font-size: 0.82rem;
            line-height: 1.5;
            margin-top: 1.2rem;
        }

        .stButton > button {
            border-radius: 17px !important;
            border: 1px solid var(--fs-border) !important;
            background: rgba(255,252,247,0.94) !important;
            color: var(--fs-text) !important;
            font-weight: 800 !important;
            padding: 0.68rem 0.9rem !important;
            min-height: 3rem;
            box-shadow: 0 10px 24px rgba(23, 23, 23, 0.04);
            transition: all 0.15s ease-in-out;
        }

        .stButton > button:hover {
            border-color: rgba(46, 125, 91, 0.46) !important;
            color: var(--fs-green-dark) !important;
            transform: translateY(-1px);
            box-shadow: 0 14px 30px rgba(46, 125, 91, 0.10);
        }

        .stTextArea textarea {
            background: rgba(255, 252, 247, 0.98) !important;
            color: var(--fs-text) !important;
            border: 1px solid var(--fs-border) !important;
            border-radius: 18px !important;
            padding: 0.9rem !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.55);
        }

        .stTextArea textarea:focus {
            border-color: rgba(46, 125, 91, 0.5) !important;
            box-shadow: 0 0 0 3px rgba(46, 125, 91, 0.09) !important;
        }

        div[data-testid="stExpander"] {
            background: rgba(255, 252, 247, 0.85);
            border: 1px solid var(--fs-border);
            border-radius: 16px;
            overflow: hidden;
        }

        div[data-testid="stExpander"] summary {
            color: var(--fs-text);
            font-weight: 800;
        }

        @media (max-width: 980px) {
            .fs-card-grid {
                grid-template-columns: 1fr;
            }

            .fs-title {
                font-size: 2.45rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Componentes visuales
# ============================================================

def render_hero():
    st.markdown(
        """
        <div class="fs-hero">
            <div class="fs-eyebrow">💊 MVP académico · Gemini · ChromaDB · LangGraph</div>
            <h1 class="fs-title">FarmaStock AI</h1>
            <div class="fs-subtitle">
                Asistente RAG para optimización de stock en farmacia comunitaria.
                Recupera contexto documental propio y genera respuestas sobre rotación,
                cobertura, reposición, ABC/XYZ y movimientos de inventario.
            </div>
            <div class="fs-badge-row">
                <span class="fs-badge">Base documental propia</span>
                <span class="fs-badge">RAG con fuentes</span>
                <span class="fs-badge">Memoria conversacional</span>
                <span class="fs-badge">Sin datos reales sensibles</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_limit_banner():
    st.markdown(
        """
        <div class="fs-limit-banner">
            <strong>Ámbito de uso:</strong>
            FarmaStock AI tiene un enfoque logístico y formativo.
            No proporciona consejo clínico, no recomienda medicamentos y no toma decisiones automáticas de compra.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_cards():
    st.markdown(
        """
        <div class="fs-card-grid">
            <div class="fs-card">
                <div class="fs-card-icon">📚</div>
                <div class="fs-card-title">Base documental propia</div>
                <div class="fs-card-text">
                    4 documentos Markdown diseñados para alimentar un sistema RAG acotado al dominio.
                </div>
            </div>
            <div class="fs-card">
                <div class="fs-card-icon">🔎</div>
                <div class="fs-card-title">RAG con ChromaDB</div>
                <div class="fs-card-text">
                    Recupera fragmentos relevantes antes de generar cada respuesta con Gemini.
                </div>
            </div>
            <div class="fs-card">
                <div class="fs-card-icon">🧠</div>
                <div class="fs-card-title">Memoria conversacional</div>
                <div class="fs-card-text">
                    Mantiene el contexto entre turnos mediante LangGraph y thread_id.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_title(title: str, subtitle: str = ""):
    st.markdown(f'<div class="fs-section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="fs-section-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def render_sidebar_value(label: str, value: str):
    st.markdown(f'<div class="fs-sidebar-label">{label}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="fs-sidebar-value">{value}</div>', unsafe_allow_html=True)


def render_source_cards(sources: List[Dict[str, str]]):
    if not sources:
        st.markdown('<div class="fs-small-muted">No hay fuentes recuperadas.</div>', unsafe_allow_html=True)
        return

    for i, source in enumerate(sources, start=1):
        st.markdown(
            f"""
            <div class="fs-source-card">
                <strong>Fuente {i}</strong><br>
                <span class="fs-small-muted">Documento:</span> <code>{source['document_id']}</code><br>
                <span class="fs-small-muted">Sección:</span> {source['section_title']}<br>
                <span class="fs-small-muted">Chunk:</span> <code>{source['chunk_id']}</code>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_chat_message(role: str, content: str, sources: Optional[List[Dict[str, str]]] = None):
    """
    Renderiza mensajes con una cabecera visual y el contenido debajo.
    Mantiene el Markdown de las respuestas y evita abrir/cerrar divs alrededor de componentes Streamlit.
    """
    if role == "user":
        label = "👤 Tú"
        css_class = "fs-chat-user"
    else:
        label = "💊 FarmaStock AI"
        css_class = "fs-chat-assistant"

    with st.container():
        st.markdown(
            f"""
            <div class="fs-chat-box {css_class}">
                <div class="fs-chat-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=False):
            st.markdown(content)

        if role == "assistant" and sources:
            with st.expander("Fuentes recuperadas"):
                render_source_cards(sources)


def extract_sources(result: Dict[str, Any]) -> List[Dict[str, str]]:
    retrieved_docs = result.get("retrieved_docs", [])
    sources = []

    for doc in retrieved_docs:
        metadata = doc.metadata
        sources.append(
            {
                "document_id": metadata.get("document_id", "documento_desconocido"),
                "section_title": metadata.get("section_title", "sección_desconocida"),
                "chunk_id": metadata.get("chunk_id", "chunk_desconocido"),
            }
        )

    return sources


# ============================================================
# Configuración Streamlit
# ============================================================

st.set_page_config(
    page_title="FarmaStock AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()


# ============================================================
# Inicialización de estado visual
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"streamlit_demo_{uuid.uuid4().hex[:8]}"

if "last_sources" not in st.session_state:
    st.session_state.last_sources = []


# ============================================================
# Carga del agente
# ============================================================

try:
    app, vectorstore = load_agent()
    collection_count = vectorstore._collection.count()
    agent_loaded = True

except Exception as e:
    agent_loaded = False
    collection_count = 0
    load_error = e


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.markdown("## FarmaStock AI")
    st.caption("Panel técnico de la demo")

    st.markdown("---")

    st.markdown("### Configuración del modelo")
    render_sidebar_value("LLM", GEMINI_LLM_MODEL)
    render_sidebar_value("Embeddings", EMBEDDING_MODEL)
    render_sidebar_value("Temperatura", str(TEMPERATURE))

    st.markdown("---")

    st.markdown("### Recuperación RAG")
    render_sidebar_value("Colección", COLLECTION_NAME)
    render_sidebar_value("Retriever", f"similarity | k={RETRIEVER_K}")
    render_sidebar_value("Chunks indexados", str(collection_count) if agent_loaded else "No disponible")

    st.markdown("---")

    st.markdown("### Base documental")

    expected_docs = [
        "01_fundamentos_stock_farmacia.md",
        "02_metricas_reposicion_farmacia.md",
        "03_clasificacion_abc_xyz_farmacia.md",
        "04_interpretacion_movimientos_stock.md",
    ]

    for doc_name in expected_docs:
        doc_path = DATA_DIR / doc_name
        css_class = "fs-doc-item" if doc_path.exists() else "fs-doc-item fs-doc-missing"
        prefix = "✓" if doc_path.exists() else "!"
        st.markdown(
            f'<div class="{css_class}">{prefix} {doc_name}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown("### Estado")
    if agent_loaded:
        st.markdown('<span class="fs-pill">Agente cargado</span>', unsafe_allow_html=True)
        st.markdown('<span class="fs-pill">ChromaDB disponible</span>', unsafe_allow_html=True)

        if collection_count == 117:
            st.markdown('<span class="fs-pill">Vectorstore validado</span>', unsafe_allow_html=True)
        else:
            st.warning(
                f"ChromaDB contiene {collection_count} chunks. "
                "Se esperaban 117. Reconstruye la base desde el notebook si detectas duplicados."
            )
    else:
        st.markdown('<span class="fs-pill">Error de carga</span>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Conversación")

    if st.button("Borrar conversación", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_sources = []
        st.session_state.thread_id = f"streamlit_demo_{uuid.uuid4().hex[:8]}"
        st.rerun()


# ============================================================
# Control de errores de carga
# ============================================================

if not agent_loaded:
    render_hero()
    st.error("No se ha podido cargar FarmaStock AI.")
    st.exception(load_error)
    st.stop()


# ============================================================
# Layout principal
# ============================================================

render_hero()
render_limit_banner()
render_info_cards()

left_col, right_col = st.columns([1.45, 0.85], gap="large")


# ============================================================
# Panel izquierdo: Chat
# ============================================================

with left_col:
    render_section_title(
        "Chat",
        "Pregunta al asistente sobre gestión logística de stock. El agente recupera contexto documental antes de responder.",
    )

    if not st.session_state.messages:
        st.markdown(
            """
            <div class="fs-empty-chat">
                Todavía no hay conversación. Puedes escribir una pregunta o usar una de las preguntas sugeridas del panel derecho.
                <br><br>
                Para la demo, prueba primero con una pregunta conceptual y después con una pregunta de cálculo o memoria.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for message in st.session_state.messages:
            render_chat_message(
                role=message["role"],
                content=message["content"],
                sources=message.get("sources"),
            )

    st.markdown('<div class="fs-divider"></div>', unsafe_allow_html=True)

    with st.form("question_form", clear_on_submit=True):
        question = st.text_area(
            "Escribe tu pregunta",
            placeholder="Ejemplo: ¿Qué diferencia hay entre rotación y cobertura de stock?",
            height=110,
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button("Enviar pregunta", use_container_width=True)

    prompt_to_process = question.strip() if submitted and question.strip() else None


# ============================================================
# Panel derecho: demo, sugerencias y fuentes
# ============================================================

with right_col:
    st.markdown(
        """
        <div class="fs-panel-static">
            <div class="fs-panel-title">Preguntas sugeridas</div>
            <div class="fs-panel-caption">
                Diseñadas para demostrar recuperación documental, razonamiento, memoria y límites del agente.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    suggested_questions = [
        "¿Qué diferencia hay entre rotación y cobertura de stock?",
        "Si un producto tiene 24 unidades disponibles y vende 3 unidades al día, ¿qué cobertura aproximada tiene?",
        "¿Qué diferencia hay entre un producto AX y un producto AZ?",
        "Si el stock anterior era 5 y el stock posterior es 12 tras una modificación manual, ¿cómo se interpreta?",
        "Explícame qué es la cobertura de stock.",
        "¿Qué medicamento recomiendas para un resfriado?",
    ]

    selected_suggestion = None

    for i, suggested in enumerate(suggested_questions):
        if st.button(suggested, key=f"suggested_{i}", use_container_width=True):
            selected_suggestion = suggested

    st.markdown(
        """
        <div class="fs-panel-static" style="margin-top: 1rem;">
            <div class="fs-panel-title">Últimas fuentes recuperadas</div>
            <div class="fs-panel-caption">
                Se muestran documento, sección y chunk utilizado por el retriever.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.last_sources:
        with st.expander("Ver fuentes de la última respuesta", expanded=True):
            render_source_cards(st.session_state.last_sources)
    else:
        st.markdown(
            '<div class="fs-small-muted">Aún no hay fuentes. Realiza una pregunta para ver la recuperación RAG.</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="fs-panel-static" style="margin-top: 1rem;">
            <div class="fs-panel-title">Guion rápido de demo</div>
            <div class="fs-panel-caption">
                1. Pregunta conceptual.<br>
                2. Pregunta con cálculo sencillo.<br>
                3. ABC/XYZ.<br>
                4. Modificación manual y delta.<br>
                5. Pregunta de memoria.<br>
                6. Pregunta fuera de dominio.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if selected_suggestion:
    prompt_to_process = selected_suggestion


# ============================================================
# Procesamiento de la pregunta
# ============================================================

if prompt_to_process:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt_to_process,
        }
    )

    with st.spinner("Recuperando contexto documental y generando respuesta..."):
        try:
            result = run_agent(
                app=app,
                mensaje=prompt_to_process,
                thread_id=st.session_state.thread_id,
            )

            answer = result["answer"]
            sources = extract_sources(result)

            st.session_state.last_sources = sources

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                }
            )

            st.rerun()

        except Exception as e:
            st.error("Ha ocurrido un error al generar la respuesta.")
            st.exception(e)


# ============================================================
# Pie de página
# ============================================================

st.markdown('<div class="fs-divider"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="fs-footer">
        FarmaStock AI — MVP académico con Gemini, RAG, ChromaDB, LangGraph y memoria conversacional.
        La interfaz Streamlit actúa como capa visual opcional sobre el notebook técnico ya validado.
    </div>
    """,
    unsafe_allow_html=True,
)