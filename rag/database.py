from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from pathlib import Path
import hashlib

from utils.agent_call import gemini_client

# Function add particular folder to db
def index_folder(folder_path, collection_name):
    # Load all markdown files from folders
    loader = DirectoryLoader(
        folder_path, 
        glob="**/*.md", 
        loader_cls=UnstructuredMarkdownLoader
    )
    
    raw_documents = loader.load()
    # Split into chunks
    final_documents = split_text(raw_documents)
    # Embed and add to db
    db = get_db(collection_name)
    db = add_to_db(db, final_documents)

    return db

# Function: Splits data into chunks
def split_text(raw_documents):

    # MarkdownHeaderTextSplitter preserves document structure based on headers (#, ##)
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    # Recursive splitter breaks down chunks further if they exceed the target size
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )

    final_documents = []
    for doc in raw_documents:
        # Split by markdown headers first
        header_splits = markdown_splitter.split_text(doc.page_content)
        # Ensure source metadata carries over
        for split in header_splits:
            split.metadata["source"] = doc.metadata.get("source", "Unknown")
        
        # Sub-split into uniform chunk sizes
        chunks = text_splitter.split_documents(header_splits)
        final_documents.extend(chunks)

    return final_documents

# Function: Embeds Data using Gemini Embeddings API
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Use the Gemini Embeddings API to generate embeddings for the input documents
        result = gemini_client.models.embed_content(
            model="gemini-embedding-2",
            contents=input,
        )  

        return [embedding.values for embedding in result.embeddings]

# Function: Create a persistent Chroma client and collection
def get_db(db_name):

    client = chromadb.PersistentClient(path="data/")

    try:
        return client.get_collection(
            f"{db_name}_collection",
            embedding_function=GeminiEmbeddingFunction()
        )

    except:
        return client.create_collection(
            f"{db_name}_collection",
            embedding_function=GeminiEmbeddingFunction()
        )

# Function: Stores Data in ChromaDB
def add_to_db(db, documents):

    for i, doc in enumerate(documents):

        source = Path(doc.metadata["source"]).name

        metadata = {
            "source": str(source),
            "chunk": int(i),
            "header1": str(doc.metadata.get("Header 1", "")),
            "header2": str(doc.metadata.get("Header 2", "")),
            "header3": str(doc.metadata.get("Header 3", "")),
        }

        doc_id = hashlib.sha256(doc.page_content.encode()).hexdigest()

        db.add(documents=[doc.page_content], 
               ids = [f"{source}_{doc_id}"],
               metadatas=[metadata]
                )

    return db

# Retrieving Relevant Passages from ChromaDB
def retrieve(query, db, k=4):

    return db.query(
        query_texts=[query],
        n_results=k
    )