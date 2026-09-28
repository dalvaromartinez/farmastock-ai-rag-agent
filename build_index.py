from pathlib import Path
import os
import re
import shutil
import time
from typing import Any, Dict, List, Tuple

import yaml
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


# ============================================================
# Configuración general
# ============================================================

PROJECT_NAME = "FarmaStock Knowledge Assistant"
PROJECT_DOMAIN = "Optimización de stock en farmacia comunitaria"

COLLECTION_NAME = "farmastock_ai_docs"
EMBEDDING_MODEL = "models/gemini-embedding-001"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

BATCH_SIZE = 30
SLEEP_SECONDS = 65


# ============================================================
# Rutas
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"
CHROMA_DIR = BASE_DIR / "chroma_db"

EXPECTED_FILES = [
    "01_fundamentos_stock_farmacia.md",
    "02_metricas_reposicion_farmacia.md",
    "03_clasificacion_abc_xyz_farmacia.md",
    "04_interpretacion_movimientos_stock.md",
]


# ============================================================
# Metadatos requeridos
# ============================================================

REQUIRED_YAML_KEYS = [
    "title",
    "document_id",
    "version",
    "domain",
    "use_in_rag",
    "contains_real_data",
]

REQUIRED_CHUNK_METADATA = [
    "title",
    "document_id",
    "version",
    "domain",
    "use_in_rag",
    "contains_real_data",
    "source",
    "filename",
    "section_number",
    "section_title",
    "chunk_index",
    "chunk_id",
    "doc_type",
    "created_for",
]


# ============================================================
# Carga documental
# ============================================================

def read_markdown_file(path: Path) -> str:
    """Lee un documento Markdown en UTF-8."""
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo requerido: {path.name}")

    return path.read_text(encoding="utf-8")


def extract_yaml_metadata(text: str) -> Tuple[Dict[str, Any], str]:
    """
    Extrae el front matter YAML inicial.

    Devuelve:
    - metadata
    - cuerpo Markdown sin el front matter
    """
    if not text.startswith("---"):
        raise ValueError(
            "El documento no empieza con una cabecera YAML delimitada por ---."
        )

    parts = text.split("---", 2)

    if len(parts) < 3:
        raise ValueError(
            "No se ha podido cerrar correctamente la cabecera YAML."
        )

    yaml_text = parts[1].strip()
    body = parts[2].strip()

    metadata = yaml.safe_load(yaml_text)

    if metadata is None:
        metadata = {}

    missing_keys = [
        key for key in REQUIRED_YAML_KEYS
        if key not in metadata
    ]

    if missing_keys:
        raise ValueError(
            "Faltan claves obligatorias en la cabecera YAML: "
            + ", ".join(missing_keys)
        )

    return metadata, body


def load_documents() -> List[Dict[str, Any]]:
    """
    Carga y valida los cuatro documentos definidos para el proyecto.
    """
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            "No existe data/raw/. "
            "Comprueba la estructura del repositorio."
        )

    document_paths = [
        DATA_DIR / filename
        for filename in EXPECTED_FILES
    ]

    missing_files = [
        path.name
        for path in document_paths
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Faltan documentos obligatorios en data/raw/: "
            + ", ".join(missing_files)
        )

    parsed_docs: List[Dict[str, Any]] = []

    for path in document_paths:
        raw_text = read_markdown_file(path)
        metadata, body = extract_yaml_metadata(raw_text)

        if metadata.get("domain") != PROJECT_DOMAIN:
            raise ValueError(
                f"El documento {metadata.get('document_id', path.name)} "
                f"tiene un dominio inesperado: {metadata.get('domain')}"
            )

        metadata["source"] = path.relative_to(BASE_DIR).as_posix()
        metadata["filename"] = path.name

        parsed_docs.append(
            {
                "metadata": metadata,
                "body": body,
            }
        )

    return parsed_docs


# ============================================================
# Secciones Markdown
# ============================================================

def split_markdown_sections(body: str) -> List[Dict[str, str]]:
    """
    Divide un documento utilizando encabezados Markdown de nivel 2.
    """
    pattern = r"(?m)^##\s+(.+)$"
    matches = list(re.finditer(pattern, body))

    if not matches:
        raise ValueError(
            "No se encontraron secciones con encabezado ## en el documento."
        )

    sections: List[Dict[str, str]] = []

    for index, match in enumerate(matches):
        section_title = match.group(1).strip()
        start = match.start()
        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(body)
        )

        section_text = body[start:end].strip()

        number_match = re.match(r"^(\d+)\.", section_title)
        section_number = (
            number_match.group(1)
            if number_match
            else str(index + 1)
        )

        sections.append(
            {
                "section_number": section_number,
                "section_title": section_title,
                "section_text": section_text,
            }
        )

    return sections


def build_sections(
    parsed_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Construye las secciones que pueden utilizarse en RAG.

    Solo se indexan documentos con use_in_rag: true.
    También se excluyen las secciones de preguntas que el
    notebook actual ya excluye de la indexación.
    """
    sections: List[Dict[str, Any]] = []

    for doc in parsed_docs:
        doc_metadata = doc["metadata"]

        if doc_metadata.get("use_in_rag") is not True:
            print(
                "Documento excluido de RAG por metadata: "
                f"{doc_metadata.get('document_id', 'desconocido')}"
            )
            continue

        doc_sections = split_markdown_sections(doc["body"])

        for section in doc_sections:
            section_title_lower = section["section_title"].lower()

            if "preguntas que puede responder" in section_title_lower:
                continue

            section_metadata = {
                **doc_metadata,
                "section_number": section["section_number"],
                "section_title": section["section_title"],
            }

            sections.append(
                {
                    "text": section["section_text"],
                    "metadata": section_metadata,
                }
            )

    if not sections:
        raise ValueError(
            "No hay secciones disponibles para indexar."
        )

    return sections


# ============================================================
# Limpieza
# ============================================================

def clean_text(text: str) -> str:
    """
    Aplica la misma limpieza básica del notebook sin destruir
    la estructura Markdown.
    """
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    return text.strip()


# ============================================================
# Chunking
# ============================================================

def build_chunk_text(
    section_text: str,
    metadata: Dict[str, Any],
) -> str:
    """
    Añade contexto documental antes de dividir cada sección.
    """
    document_title = metadata.get(
        "title",
        "Documento sin título",
    )
    section_title = metadata.get(
        "section_title",
        "Sección sin título",
    )

    return (
        f"Documento: {document_title}\n"
        f"Sección: {section_title}\n\n"
        f"{section_text}"
    )


def build_chunks(
    sections: List[Dict[str, Any]],
) -> List[Document]:
    """
    Divide las secciones mediante RecursiveCharacterTextSplitter.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks: List[Document] = []

    for section in sections:
        section_text = clean_text(section["text"])
        section_metadata = section["metadata"]

        text_with_context = build_chunk_text(
            section_text,
            section_metadata,
        )

        split_texts = text_splitter.split_text(
            text_with_context
        )

        for chunk_index, chunk_text in enumerate(split_texts):
            document_id = section_metadata["document_id"]
            section_number = section_metadata["section_number"]

            chunk_metadata = {
                **section_metadata,
                "chunk_index": chunk_index,
                "chunk_id": (
                    f"{document_id}"
                    f"__section_{section_number}"
                    f"__chunk_{chunk_index:03d}"
                ),
                "doc_type": "technical_training",
                "created_for": PROJECT_NAME,
                "chunk_size": CHUNK_SIZE,
                "chunk_overlap": CHUNK_OVERLAP,
            }

            chunks.append(
                Document(
                    page_content=chunk_text,
                    metadata=chunk_metadata,
                )
            )

    if not chunks:
        raise ValueError(
            "No se ha generado ningún chunk."
        )

    for chunk in chunks:
        missing = [
            key
            for key in REQUIRED_CHUNK_METADATA
            if key not in chunk.metadata
        ]

        if missing:
            raise ValueError(
                "El chunk "
                f"{chunk.metadata.get('chunk_id', 'sin_id')} "
                "no contiene metadatos obligatorios: "
                + ", ".join(missing)
            )

    return chunks


def validate_unique_chunk_ids(chunks: List[Document]) -> None:
    """
    Comprueba que cada chunk_id sea único antes de crear embeddings.
    """
    chunk_ids = [
        chunk.metadata["chunk_id"]
        for chunk in chunks
    ]

    if len(chunk_ids) != len(set(chunk_ids)):
        raise RuntimeError(
            "La validación de chunk_id ha fallado: "
            f"se generaron {len(chunk_ids)} chunks, "
            f"pero solo {len(set(chunk_ids))} chunk_id son únicos."
        )


# ============================================================
# Reconstrucción limpia de ChromaDB
# ============================================================

def reset_vectorstore() -> None:
    """
    Elimina completamente el índice persistente anterior.

    Si la eliminación falla, el proceso se detiene.
    Nunca se continúa indexando sobre una ChromaDB que no
    haya podido limpiarse correctamente.
    """
    if not CHROMA_DIR.exists():
        return

    print("Eliminando índice ChromaDB anterior...")

    try:
        shutil.rmtree(CHROMA_DIR)
    except OSError as exc:
        raise RuntimeError(
            "No se ha podido eliminar chroma_db. "
            "Cierra cualquier proceso que esté usando el índice "
            "y vuelve a ejecutar el builder."
        ) from exc

    if CHROMA_DIR.exists():
        raise RuntimeError(
            "chroma_db sigue existiendo después del intento "
            "de limpieza. Se aborta la reconstrucción."
        )

    print("Índice anterior eliminado correctamente.")


# ============================================================
# Embeddings e indexación
# ============================================================

def build_vectorstore(
    chunks: List[Document],
) -> Chroma:
    """
    Construye desde cero la colección persistente de ChromaDB.
    """
    load_dotenv()

    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not google_api_key:
        raise ValueError(
            "No se ha encontrado GOOGLE_API_KEY. "
            "Crea un archivo .env en la raíz del proyecto "
            "antes de construir el índice."
        )

    reset_vectorstore()

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=google_api_key,
    )

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    total_chunks = len(chunks)

    for start in range(0, total_chunks, BATCH_SIZE):
        end = min(start + BATCH_SIZE, total_chunks)
        batch = chunks[start:end]

        print(
            f"Indexando chunks {start + 1}-{end} "
            f"de {total_chunks}..."
        )

        vectorstore.add_documents(batch)

        if end < total_chunks:
            print(
                f"Esperando {SLEEP_SECONDS} segundos "
                "antes del siguiente lote..."
            )
            time.sleep(SLEEP_SECONDS)

    collection_count = vectorstore._collection.count()

    if collection_count != len(chunks):
        raise RuntimeError(
            "La validación del índice ha fallado: "
            f"se generaron {len(chunks)} chunks, "
            f"pero ChromaDB contiene {collection_count} registros."
        )

    print(
        "Índice construido correctamente: "
        f"{collection_count} chunks en la colección "
        f"{COLLECTION_NAME}."
    )

    return vectorstore


# ============================================================
# Entrada
# ============================================================

def main() -> None:
    print(f"Proyecto: {PROJECT_NAME}")
    print(f"Modelo de embeddings: {EMBEDDING_MODEL}")
    print(
        f"Chunking: size={CHUNK_SIZE}, "
        f"overlap={CHUNK_OVERLAP}"
    )

    parsed_docs = load_documents()

    rag_docs = [
        doc
        for doc in parsed_docs
        if doc["metadata"].get("use_in_rag") is True
    ]

    print(
        f"Documentos disponibles: {len(parsed_docs)}"
    )
    print(
        f"Documentos habilitados para RAG: {len(rag_docs)}"
    )

    sections = build_sections(parsed_docs)

    print(
        f"Secciones preparadas para indexación: {len(sections)}"
    )

    chunks = build_chunks(sections)

    print(f"Chunks generados: {len(chunks)}")

    validate_unique_chunk_ids(chunks)

    print(
        f"Chunk IDs únicos validados: {len(chunks)}"
    )

    build_vectorstore(chunks)


if __name__ == "__main__":
    main()
