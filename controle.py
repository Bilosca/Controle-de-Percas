import sqlite3
import datetime

class PerdasDB:
    def __init__(self, arquivoDB):
        self.conex = sqlite3.connect(arquivoDB)
        self.cursor = self.conex.cursor()
        self.cursor2 = self.conex.cursor()
        self.cursor3 = self.conex.cursor()


    # Metodo para inserir uma remessa no Banco de Dados, recebe:
    # o nome do produto, o setor, dia de validade, mes e ano.
    def insere_remessa(self, produto, setor, dia, mes, ano):
        try:
            validade_data = datetime.date(ano, mes, dia)

            global atual
            atual = datetime.date.today()

            diferenca = abs((validade_data - atual).days)

            query = 'INSERT INTO remessas(produto, setor, validade, dias) VALUES (?, ?, ?, ?)'

            self.cursor.execute(query, (produto, setor, validade_data, diferenca))
            self.conex.commit()
            print("Produto inserido com sucesso")

        except Exception as error:
            print(error)
            pass

    
    # Metodo para pegar a data de validade e retornar a diferenca de dias para vencimento
    def organiza_Datas(self, ident):

        try:
            select_data_query = "SELECT validade FROM remessas WHERE id LIKE ?"            

            
            data = self.cursor.execute(select_data_query, (ident,)).fetchone()

            atual = datetime.date.today()

            # ja que o fetch pega tuplas, eu converti a tupla em string e fatiei a string em varios ints diferentes
            
            data_string = data[0]
            

            ano = int(data_string[:4])
            mes = int(data_string[5:7])
            dia = int(data_string[8:10])

            data = datetime.date(ano, mes, dia)
            
            diferenca = abs((data - atual).days)

            return diferenca
        except TypeError:
            pass
        

    def atualizaDias_e_Notifica(self):

        #queries utilizadas nesta funcao
        select_id_query = "SELECT id, produto FROM remessas"
        update_dias_query = "UPDATE remessas SET dias = ? WHERE id = ?"
        delete_query = "DELETE FROM remessas WHERE id = ? "

        try:
            self.cursor.execute(select_id_query,)
            coluna_dias = self.cursor.fetchall()

            # a cada loop "Ident" recebe o ID da remessa
            for row in coluna_dias:
                #row[0] = id
                #row[1] = nome do produto 
                ident = row[0]
                produto = row[1]

                diferenca = (self.organiza_Datas(ident))
                if diferenca <= 30:
                    print(f"ID: {ident} \nProduto: {produto} \nDias: { diferenca} \n")
                
                if diferenca <= 0:
                    print(f"Produto Deletado! \nID: {ident} \nProduto: {produto}")
                    self.cursor3.execute(delete_query, (ident,))

                
                self.cursor2.execute(update_dias_query, (diferenca, ident))
                self.conex.commit()

        
        except Exception as erro:
            print(erro)

    # Metodo para Excluir uma remessa do Banco de Dados, recebe como parametro o ID da remessa
    def exclui_remessa(self, ident):
        query = 'DELETE FROM remessas WHERE id = ?'

        self.cursor.execute(query,(ident,))
        self.conex.commit()
        print("Produto deletado com sucesso")

    # Metodo para editar uma remessa do Banco de Dados, recebe como parametros, id, produto e setor
    def editar_remessa(self, ident, produto, setor, ):
        query = 'UPDATE remessas SET produto = ?, setor = ? WHERE id = ?'

        self.cursor.execute(query, (produto, setor, ident))
        self.conex.commit()
        print("Produto editado com sucesso")

    #METODO QUE BUSCA A REMESSA DO PRODUTO DE ACORDO COM O NOME DO PRODUTO
    def buscar_produto(self, produto):
        query = 'SELECT * FROM remessas WHERE produto LIKE ?'

        self.cursor.execute(query, (f"%{produto}%",))

        for produto in self.cursor.fetchall():
            print(produto)


    def fechar(self):
        self.cursor.close()
        self.conex.close()

# FUNCAO QUE PEGA OS DADOS DO PRODUTO E RETORNA PARA VARIAVEIS
""" Caso o Parametro seja (1), a funcao so retornara o {Produto, Setor}, e caso o Parametro seja (0)
    Retornara {Produto, Setor, Dia, Mes, Ano}."""
def insere_dados(opcao = 0):
    produto = input('NOME DO PRODUTO: ')

    if opcao == 0:
        setor = input('SETOR DO PRODUTO: ')
        dia = int(input('DIA: '))
        mes = int(input('MES: '))
        ano = int(input('ANO: '))
        return produto, setor, dia, mes, ano

    elif opcao == 1:
        setor = input('SETOR DO PRODUTO: ')
        ident = int(input('Id: '))
        return ident, produto, setor

    elif opcao == 2:
        return produto


if __name__ == "__main__":
    perdas = PerdasDB('/home/gabe/Desktop/treinamento/perdas/controle_perdas.db')
    letras = ['i', 'e', 'b', 'd', 'f']
    perdas.atualizaDias_e_Notifica()
    while True:
        print("\nPressione a Letra pra escolher sua opcao: ")
        print()

        try:
            decision = input("(I) - Inserir Remessa \n(E) - Editar Remessa \n(B) - Buscar Remessa\
                \n(D) - Deletar Remessa \n(F) - Fechar Programa \n\n")
            
            decision = decision.lower()

            if decision not in letras:
                print("(Opcao Nao disponivel !)\n")
                continue

            if decision == 'i':
                print("\nRegras: \n1° - Nome \n2° - Marca \n")
                produto, setor, dia, mes, ano = insere_dados(0)
                perdas.insere_remessa(produto, setor, dia, mes, ano)
            
            elif decision =='e':
                ident, produto, setor = insere_dados(1)
                perdas.editar_remessa(ident, produto, setor)
            
            elif decision == 'b':
                produto = insere_dados(2)
                perdas.buscar_produto(produto)

            elif decision == 'd':
                ident = input("Id da Remessa: ")
                perdas.exclui_remessa(ident)
                        
            elif decision == 'f':
                perdas.fechar()
                break

        except Exception as erro:
            print(erro)
            pass 

