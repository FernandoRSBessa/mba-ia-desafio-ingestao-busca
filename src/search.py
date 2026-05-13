import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def validate_env():
    for k in ("DATABASE_URL","PG_VECTOR_COLLECTION_NAME"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

def get_embeddings_model():
    model_strategy = os.getenv("MODEL_STRATEGY", "openai")
    if model_strategy == "gemini":
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-2-preview"))
    else:
        return OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))
  
def get_chat_model():
    model_strategy = os.getenv("MODEL_STRATEGY", "openai")
    if model_strategy == "gemini":
        return ChatGoogleGenerativeAI(model=os.getenv("LLM_MODEL", "gemini-3.1-flash-lite"), temperature=float(os.getenv("LLM_TEMPERATURE", "0.5")))
    else:
        return ChatOpenAI(model=os.getenv("LLM_MODEL", "gpt-5-mini"), temperature=float(os.getenv("LLM_TEMPERATURE", "0.5")))

def search_prompt(question=None):
    if not question:
        raise ValueError("Nenhuma questão a ser respondida.")
    validate_env()
    store = PGVector(
        embeddings=get_embeddings_model(),
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    results = store.similarity_search_with_score(question, k=10)
    if not results:
        print("Nenhum resultado encontrado para a pergunta.")
        return

    # fazer chamada à LLM usando o PROMPT_TEMPLATE, passando os resultados da busca como contexto e a pergunta do usuário como pergunta a ser respondida
    question_template = PromptTemplate(
      input_variables=["contexto", "pergunta"],
      template=PROMPT_TEMPLATE
    )

    model = get_chat_model()

    chain = question_template | model

    return chain.invoke({"contexto": results, "pergunta": question})    