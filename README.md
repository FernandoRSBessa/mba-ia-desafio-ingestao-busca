# Desafio MBA Engenharia de Software com IA - Full Cycle

Projeto consiste em ler um PDF salvando suas informações em um banco de dados PostgreSql com extensão pgVector e disponibilizar um chat para fazer perguntas referentes ao conteúdo desse PDF.

## Estrutura do Projeto

Este projeto tem **3 arquivos** principais:

1. **ingest.py** - Script de ingestão do PDF
2. **search.py** - Script de busca no banco vetorial e resposta à pergunta através de LLM com base nas informações obtidas no banco vetorial
3. **chat.py** - CLI para interação com usuário

---

## Instruções de execução

### Pré-requisitos

```bash
# 1. Criar virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependências (do requirements.txt local)
pip install -r requirements.txt

# 3. Subir o banco de dados
docker compose up -d
```

### Variáveis de Ambiente

- Criar arquivo `.env` na raiz com base no `.env.example`
- Fazer os devidos ajustes nas variáveis de ambiente conforme o necessário
- A variável MODEL_STRATEGY pode receber os valores "gemini" ou "openai", para determinar qual provedora de modelo será utilizada.
- Conforme o MODEL_STRATEGY escolhido, preencher a API_KEY correspondente

### Ordem de execução

1. Executar ingestão do PDF:
    ```
    python src/ingest.py
    ```
2. Rodar o chat:
    ```
    python src/chat.py
    ```