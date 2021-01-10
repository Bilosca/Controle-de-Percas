from controle_metodos import PerdasDB, insereDados
import os

#Arquivo principal cujo o programa importa as classes e metodos e roda

if not os.path.exists("perdas"):
    os.mkdir("perdas")

perdas = PerdasDB("perdas/controle_perdas.db")
letras = ['i', 'e', 'b', 'd', 'f']
perdas.atualizaDias_e_Notifica()
while True:
    print("\n\nPressione a Letra pra escolher sua opcao: ")
    print()

    try:
        decision = input("(I) - Inserir Remessa \n(E) - Editar Remessa \n(B) - Buscar Remessa\
            \n(D) - Deletar Remessa \n(F) - Fechar Programa \n\n")
        
        decision = decision.lower()

        if decision not in letras:
            print("(Opcao Nao disponivel !)\n")
            continue

        if decision == 'i':
            print("\nRegras: \n1° - Nome \n2° - Marca")
            produto, setor, dia, mes, ano = insereDados(0)
            perdas.insereRemessa(produto, setor, dia, mes, ano)
        
        elif decision =='e':
            ident, produto, setor = insereDados(1)
            perdas.editarRemessa(ident, produto, setor)
        
        elif decision == 'b':
            produto = insereDados(2)
            perdas.buscarProduto(produto)

        elif decision == 'd':
            ident = input("\nId da Remessa: ")


            perdas.excluiRemessa(ident)
                    
        elif decision == 'f':
            perdas.fechar()
            break

    except Exception as erro:
        print(erro)
        pass 
