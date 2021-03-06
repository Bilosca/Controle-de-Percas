# Controle-de-Percas
## Objetivo do Projeto
Como eu trabalho com reposição de mercadorias, ocorre de haver percas, então para facilitar, organizar, e melhorar o gerenciamento do meu trabalho, além de desenvolver minhas
habilidades como programador, praticar, e aprender tecnologias que antes não tinha trabalhado.

## Como Funciona o projeto
É um projeto bastante simples em Command Line. Quando iniciado primeiramente criará a pasta "Perda" e dentro dela o arquivo "controle_perdas.db".
Para o manuseamento do Programa, ele lhe dará as seguintes opções:
* Inserir Remessa
* Editar Remessa
* Buscar Remessa
* Deletar Remessa

Para Inserir uma Remessa, é preciso inserir _Nome do Produto, Setor, Dia, Mês, e Ano_ , ele será inserido ao banco de dados, e e com o passar dos dias, o programa deve ser executado
para atualizar a Tabela com os dias restantes para o vencimento do produto.

## Tecnlogias Utilizadas
foi utilizado nesse projeto, a Linguagem de Programação Python, o modelo de Banco de Dados Relacional SQL,
usei do módulo SQLite para o Gerenciamento do Banco de Dados no código, e o "BD Browser for SQLite" para uma melhor visualização com uma Interface Gráfica.
Foi utilizado também a Bibloteca Pandas para gerar o output e visualização dos dados.

## Atualizações no código

### 09/12/20
- Me foi indicado a separar a classe e instancias das funções principais que rodam o programa, para uma melhor leitura e manutenção.
- Com o modulo "os", ao iniciar o Código, se caso não tiver a pasta "perdas" será criado, e dentro haverá o arquivo .db, com intuito de melhor organização e melhor prática.

### 13/12/2020
- foi modificado algumas váriaveis, para uma melhor leitura de código
- alterada a função "Buscar Remessa" para que mostre todos os itens do banco de dados, caso o argumento da função(Nome do Produto) seja "Todos" ou "*".

### 16/12/2020
- Alterado a forma de que os Outputs são mostrados ao entrar no programa.

### 30/12/2020
- Foi me indicado o uso de Pandas para melhor apresentação dos dados, e assim o fiz; Mudando apenas o output inicial, logo será melhor trabalhado e implementado em todo o código
- Excluido a Função "Detalhes" pois não estava sendo utilizada e bem aproveitada.

### 01/01/2021
- Modificado o output da função de Busca, implementando um DataFrame com Pandas contendo os Dados dos produtos
- Retirado o Index do DataFrame para uma visualização mais limpa e simples do do output

### 09/01/2021
- Implementado a funcionabilidade de excluir mais de um item do Banco de Dados de uma só vez, aonde basta separar os ID's por (",")
- Atualização das descrições e documentações do código e funções
