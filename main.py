import os
import sys
import gradio as gr
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as genai

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone as PineconeClient, ServerlessSpec

# 📄 Carregar PDFs
def load_pdfs(folder_path: str):
    docs = []
    for fname in os.listdir(folder_path):
        if fname.lower().endswith(".pdf"):
            path = os.path.join(folder_path, fname)
            reader = PdfReader(path)
            text = "".join(page.extract_text() or "" for page in reader.pages)
            docs.append(Document(page_content=text, metadata={"source": fname}))
    return docs

# ⚙️ Setup
load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
pinecone_cloud = os.getenv("PINECONE_CLOUD")
pinecone_region = os.getenv("PINECONE_REGION")
google_api_key = os.getenv("GEMINI_API_KEY")

if not all([pinecone_api_key, pinecone_index_name, pinecone_cloud, pinecone_region, google_api_key]):
    print("❌ Variáveis de ambiente ausentes no .env")
    sys.exit(1)

# 🔑 Configure Gemini
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemma-3-1b-it")

print("📚 Indexação Inicializada! Isto pode demorar um pouco...")

# 📦 Inicializa Pinecone
pc = PineconeClient(api_key=pinecone_api_key)
if pinecone_index_name not in pc.list_indexes().names():
    pc.create_index(
        name=pinecone_index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud=pinecone_cloud, region=pinecone_region)
    )
pinecone_index = pc.Index(pinecone_index_name)

# 📚 Indexação
raw_docs = load_pdfs("Documents")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(raw_docs)

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)

vectorstore = PineconeVectorStore(
    index=pinecone_index,
    embedding=embeddings,
    text_key="text",
    namespace="default"
)

vectorstore.add_documents(docs)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
print(f"✅ Indexação finalizada ({len(docs)} chunks no Pinecone).")

# 🤖 Função de resposta
def responder(pergunta):
    docs = retriever.get_relevant_documents(pergunta)
    contexto = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""Você é um assistente especialista em PDFs.
Use o texto abaixo para responder à pergunta com clareza e precisão.

Texto:
{contexto}

Pergunta: {pergunta}
Resposta:"""

    resposta = model.generate_content(prompt).text
    return resposta

# 🖼️ Interface Gradio
with gr.Blocks() as iface:
    gr.Markdown("# 🤖 Assistente de PDFs com Gemini (gemma-3-1b-it)")
    gr.Markdown("Faça perguntas com base nos PDFs da pasta `/Documents`.")

    with gr.Row():
        entrada = gr.Textbox(label="Pergunta", placeholder="Digite sua pergunta aqui...")
    saida = gr.Markdown(label="Resposta")

    btn = gr.Button("Responder")
    btn.click(fn=responder, inputs=entrada, outputs=saida)

# 🚀 Executar Main
if __name__ == "__main__":
    iface.launch()
