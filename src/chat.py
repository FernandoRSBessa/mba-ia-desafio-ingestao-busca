from search import search_prompt

def main():
    while True:
        print("\n\nFaça sua pergunta (ou digite 'sair' para encerrar): \n")
        pergunta = input("PERGUNTA: ")
        if pergunta.lower() == "sair":
            print("Encerrando o chat. Até a próxima!")
            break

        chain = search_prompt(pergunta)

        if not chain:
            print("RESPOSTA: Desculpe, não consegui processar sua pergunta. Tente novamente.")
        else:        
            print("RESPOSTA: " + chain.content)

if __name__ == "__main__":
    main()