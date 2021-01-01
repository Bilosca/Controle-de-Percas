import sqlite3
import datetime
import pandas as pd

#Arquivo que contem os metodos e classes

class PerdasDB:
    def __init__(self, arquivoDB):
        self.conex = sqlite3.connect(arquivoDB)
        self.cursor = self.conex.cursor()
        self.cursor2 = self.conex.cursor()
        self.cursor3 = self.conex.cursor()

        criaTabelaQuery = "CREATE TABLE IF NOT EXISTS remessas(\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        produto TEXT,\
        setor TEXT,\
        validade INTEGER,\
        dias INTEGER)"

        self.cursor.execute(criaTabelaQuery)
        self.conex.commit()

    # Metodo para inserir uma remessa no Banco de Dados, recebe:
    # o nome do produto, o setor, dia de validade, mes e ano.
    def insereRemessa(self, produto, setor, dia, mes, ano):
        try:
            validadeData = datetime.date(ano, mes, dia)

            global atual
            atual = datetime.date.today()

            diferenca = abs((validadeData - atual).days)

            query = 'INSERT INTO remessas(produto, setor, validade, dias) VALUES (?, ?, ?, ?)'

            self.cursor.execute(query, (produto, setor, validadeData, diferenca))
            self.conex.commit()
            print("\nProduto inserido com sucesso")

        except Exception as error:
            print(error)
            pass

    
    # Metodo para pegar a data de validade e retornar a diferenca de dias para vencimento
    def organizaDatas(self, ident):

        try:
            selectDataQuery = "SELECT validade FROM remessas WHERE id LIKE ?"            

            
            data = self.cursor.execute(selectDataQuery, (ident,)).fetchone()

            atual = datetime.date.today()

            # ja que o fetch pega tuplas, eu converti a tupla em string e fatiei a string em varios ints diferentes
            
            dataString = data[0]
            

            ano = int(dataString[:4])
            mes = int(dataString[5:7])
            dia = int(dataString[8:10])

            data = datetime.date(ano, mes, dia)
            
            diferenca = abs((data - atual).days)

            return diferenca
        except TypeError:
            pass

    def criaLista(self, lista,ident, produto, validade, dias, setor = None):
        if setor is None:
            lista.append({
                "ID" : ident,
                "Nome" : produto,
                "Validade" : validade,
                "Dias" : dias
            })
            return lista
        
        else:
            lista.append({
                "ID" : ident,
                "Nome" : produto,
                "Setor" : setor,
                "Validade" : validade,
                "Dias" : dias
            })
            return lista

     
    def criaDataFrame(self, lista):

        df = pd.DataFrame.from_records(lista)
        df = df.to_string(index=False)

        return df

     
    #Funcao com mais Relevancia no projeto, aonde ela atualiza a a coluna dias e informa o usuario, os produtos
    #cujo estao perto de vencimento
    def atualizaDias_e_Notifica(self):

        #queries utilizadas nesta funcao
        selectIdQuery = "SELECT id, produto, validade FROM remessas"
        updateDiasQuery = "UPDATE remessas SET dias = ? WHERE id = ?"
        deleteQuery = "DELETE FROM remessas WHERE id = ? "

        try:
            self.cursor.execute(selectIdQuery,)
            colunaDias = self.cursor.fetchall()

            print()
            print("-" *80)

            listaDados = []

            # a cada loop "Ident" recebe o ID da remessa
            for row in colunaDias:
                #row[0] = id
                #row[1] = nome do produto
                #row[2] = validade do produto
                ident = row[0]
                produto = row[1]
                validade = row[2]
                diferenca = int(self.organizaDatas(ident))


                # Caso a diferenca(dias para vencimento) seja menor ou igual a 30 dias, havera o print do ID, Produto, Dias, e Data
                if diferenca <= 30 :
                    self.criaLista(listaDados, ident, produto, validade, diferenca)

                # Caso a diferenca(dias para vencimento) seja igual a 0, a remessa e excluida do banco de dados
                if diferenca <= 0:

                    stringDelete = f"Produto Deletado! \nID: {ident} \nProduto: {produto} \nValidade: {validade}\n"
                    print(stringDelete)

                    self.cursor3.execute(deleteQuery, (ident,))
                
                
                self.cursor2.execute(updateDiasQuery, (diferenca, ident))
                self.conex.commit()

            df = self.criaDataFrame(listaDados)
            print(f"{df}")
            print("-" * 80)
        
        except Exception as erro:
            print(erro)

    # Metodo para Excluir uma remessa do Banco de Dados, recebe como parametro o ID da remessa
    def excluiRemessa(self, ident):
        query = 'DELETE FROM remessas WHERE id = ?'

        self.cursor.execute(query,(ident,))
        self.conex.commit()
        print("\nProduto deletado com sucesso")

    # Metodo para editar uma remessa do Banco de Dados, recebe como parametros, id, produto e setor
    def editarRemessa(self, ident, produto, setor, ):
        query = 'UPDATE remessas SET produto = ?, setor = ? WHERE id = ?'

        self.cursor.execute(query, (produto, setor, ident))
        self.conex.commit()
        print("\nProduto editado com sucesso")

    #METODO QUE BUSCA A REMESSA DO PRODUTO DE ACORDO COM O NOME DO PRODUTO
    #Se o nome do Produto for Todos ou *, a funcao seleciona todos os itens do banco de dados
    #Pega todos os valores na tabela, e descompacta em variaveis para uma melhor visualizacao
    def buscarProduto(self, produto):
        buscaNomeQuery = 'SELECT * FROM remessas WHERE produto LIKE ?'
        self.cursor.execute(buscaNomeQuery, (f"%{produto}%",))

        listaDados = []

        if produto == "todos" or produto == "*":
            selectTodosQuery = "SELECT * FROM remessas"
            self.cursor.execute(selectTodosQuery,)

        produtoTuple = self.cursor.fetchall()
        print("-" *80)

        for item in produtoTuple:
            ident, nome, setor, data, diasRestantes, = item
            self.criaLista(listaDados, ident, nome, data, diasRestantes, setor)

        df = self.criaDataFrame(listaDados)
        print(df)
        print("-" *80)


    def fechar(self):
        self.cursor.close()
        self.conex.close()


# FUNCAO QUE PEGA OS DADOS DO PRODUTO E RETORNA PARA VARIAVEIS
""" Caso o Parametro seja (1), a funcao so retornara o {Produto, Setor}, e caso o Parametro seja (0)
    Retornara {Produto, Setor, Dia, Mes, Ano}."""
def insereDados(opcao = 0):
    produto = input('\nNOME DO PRODUTO: ')

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


