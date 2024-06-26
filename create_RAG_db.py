from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import GPT4AllEmbeddings

from langchain_community.vectorstores.chroma import Chroma
import os
import shutil

CHROMA_PATH = "chroma_vector"
DATA_PATH = "./data/book/"

def main():
    generate_vector_store()

def generate_vector_store():
    try:
        documents = load_documents()
        chunks = split_text(documents)
        save_to_chroma(chunks)
    except Exception as e:
        print("Error: ",e)
def load_documents():
    try:
        print('loading docs..')
        loader = DirectoryLoader(DATA_PATH, glob="**/*.md", loader_cls=TextLoader)
        # loader = DirectoryLoader(DATA_PATH, glob='**/*.md', loader_cls=UnstructuredMarkdownLoader)
        documents = loader.load()
        return documents
    except Exception as e:
        print("Error: ",e)
def split_text(documents: list[Document]):
    try:

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

        document = chunks[10]
        print(document.page_content)
        print(document.metadata)
        return chunks
    except Exception as e:
        print("Error: ",e)
def save_to_chroma(chunks: list[Document]):
    try:

        # Clear out the database first.
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)

        # Create a new vector DB from the documents.
        db = Chroma.from_documents(
            documents=chunks, embedding=GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf"), persist_directory=CHROMA_PATH
        )
        # db.persist()
        print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    except Exception as e:
        print("Error: ",e)

if __name__ == "__main__":
    generate_vector_store()