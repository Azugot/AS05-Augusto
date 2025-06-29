
# 🧠 AS05 - Assistente Conversacional com LLM (LangChain + Pinecone + Gemini)

Trabalho desenvolvido para a disciplina de Tópicos Especiais em Computação III na PUC Minas.

Autor: **Augusto Scardua Oliveira**

---

## 📋 Descrição

Este projeto implementa um **assistente conversacional inteligente** que responde perguntas com base no conteúdo de arquivos PDF. Ele utiliza:

- **Pinecone** para armazenamento vetorial dos embeddings
- **HuggingFace (MiniLM)** para geração dos embeddings
- **LangChain** para orquestração do pipeline
- **Gemini (modelo Gemma-3-1b-it)** como LLM para geração das respostas
- **Gradio** para uma interface gráfica simples

---

## 🧱 Estrutura

````
AS05/
├── Documents/                 # Pasta com os arquivos PDF a serem indexados
├── main.py                   # Código principal da aplicação
├── .env                      # Variáveis de ambiente (não incluído por segurança)
├── requirements.txt          # Bibliotecas necessárias
└── README.md                 # Este guia

````

---

## ⚙️ Requisitos

- Python 3.10 ou superior
- Conta no Pinecone (e index criado)
- Chave de API do Gemini habilitada
- Internet ativa

---

## 📦 Instalação

1. Clone este repositório:

```bash
git clone <repositório>
cd AS05-Augusto
````

2. Crie um ambiente virtual (Opcional):

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie o arquivo `.env` com o seguinte conteúdo:

```
PINECONE_API_KEY=<sua-chave-pinecone>
PINECONE_INDEX_NAME=<nome-do-seu-index>
PINECONE_CLOUD=...
PINECONE_REGION=...
GEMINI_API_KEY=<sua-chave-do-gemini>
```

> ⚠️ Substitua os valores acima com suas chaves reais.

---

## 📁 Adicionando os PDFs

Coloque os arquivos `.pdf` desejados dentro da pasta `Documents/`. Eles serão automaticamente indexados ao iniciar a aplicação.

---

## ▶️ Executando o Assistente

Para iniciar a aplicação com interface gráfica:

```bash
python main.py
```

A interface será aberta automaticamente no navegador (Gradio). Você poderá fazer perguntas com base no conteúdo dos PDFs carregados.
Hospedada no URL local: " http://127.0.0.1:7860"

---

## 🧪 Exemplo de uso

```
Pergunta: Qual é a função do artigo 5º da Constituição Federal?
Resposta: [Baseada nos PDFs encontrados na pasta /Documents]
```

## 📚 Referências

* [Pinecone Docs](https://docs.pinecone.io/)
* [LangChain Docs](https://docs.langchain.com/)
* [Google Gemini](https://makersuite.google.com/app)
* [Gradio Docs](https://www.gradio.app/)

---

Aluno: **Augusto Scardua Oliveira**
