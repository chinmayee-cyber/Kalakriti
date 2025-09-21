import vertexai
from vertexai.preview import rag
from google.auth import default
from config.settings import PROJECT_ID, LOCATION, CORPUS_DISPLAY_NAME

def initialize_vertex_ai():
    creds, _ = default()
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=creds)

def create_or_get_corpus(display_name: str = CORPUS_DISPLAY_NAME):
    embedding_model_config = rag.EmbeddingModelConfig(
        publisher_model="publishers/google/models/text-embedding-004"
    )

    existing = list(rag.list_corpora())
    for c in existing:
        if c.display_name == display_name:
            return c

    corpus = rag.create_corpus(
        display_name=display_name,
        description="PoC insight cards for art valuation",
        embedding_model_config=embedding_model_config,
    )
    return corpus

def upload_text_file_to_corpus(corpus_name: str, file_path: str, display_name: str, description: str):
    rag_file = rag.upload_file(
        corpus_name=corpus_name,
        path=file_path,
        display_name=display_name,
        description=description,
    )
    return rag_file