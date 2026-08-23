"""
    Atividade Ativa - Desenvolvimento de Sistemas em Python
    Dicente: João Felipe Nascimento de Oliveira
    Professor: Francisco Lima
    Turma: Lógica- Algoritmos e Programação de Computadores [2026321]
"""

import os


# Classe para representação dos produtos no cardápio
class Produto:
    def __init__(self, codigo, nome, preco, descricao):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.descricao = descricao


# Classe para cadastro de clientes de fidelidade, a cada 10 itens comprados recebemos um valor de desconto na conta final
class Cliente:
    def __init__(self, cpf, nome, telefone):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.pontos = 0


# Imprta dados do arquivo CSV cardapio
def carregar_cardapio_csv():
    produtos = []
    # Procura o arquivo do cardápio onde o código está salvo
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(diretorio_script, "cardapio.csv")

    try:
        with open(caminho_csv, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

            for linha in linhas[1:]:
                linha_limpa = linha.strip()
                if linha_limpa:
                    partes = linha_limpa.split(";")

                    codigo = int(partes[0])
                    nome = partes[1]
                    preco = float(partes[2])
                    descricao = partes[3]

                    produtos.append(Produto(codigo, nome, preco, descricao))
    except FileNotFoundError:
        print(f'Arquivo "cardapio.csv" não encontrado na pasta: {caminho_csv}')
    except Exception as e:
        print(f"Erro ao carregar cardápio: {e} \n")

    return produtos


# Listas do sistema
cardapio = carregar_cardapio_csv()
clientes = []


# Gerar histórico de vendas

def gravar_venda(cliente_nome, itens_pedido, valor_total, desconto = 0.0):
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_relatorio = os.path.join(diretorio_script, "relatorio_tia_rosa.txt")

    try:
        with open(caminho_relatorio, "a", encoding="utf-8") as arquivo:
            arquivo.write("    Novo pedido    \n")
            arquivo.write(f"Cliente: {cliente_nome} \n")
            for item in itens_pedido:
                arquivo.write(f"-> {item.nome}: R$ {item.preco:.2f} \n")
            if desconto > 0:
                arquivo.write(f"Meus parabéns, desconto de fidelidade resgatato! \n -R$ {desconto:.2f} \n")
            arquivo.write(f"Total Final: {valor_total:.2f} \n")
            arquivo.write("--------------------\n\n")
    except Exception as e:
        print(f"Erro ao registrar venda no arquivo: {e}")


def relatorio_vendas():
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_relatorio = os.path.join(diretorio_script, "relatorio_tia_rosa.txt")

    print("\n   Histórico de Vendas   \n")
    try:
        with open(caminho_relatorio, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.readlines()
            if not conteudo:
                print("Sem vendas registradas \n")
            else:
                for linha in conteudo:
                    print(linha.strip())
    except FileNotFoundError:
        print("Arquivo de relatório ainda não foi criado \n")


# Base para exibição do cardápio
def exibir_cardapio():
    print("    Tia Rosa - Cardápio    \n")
    if not cardapio:
        print("Cardápio não encontrado... \n")
        return
    for prod in cardapio:
        print(f"{prod.codigo} | {prod.nome} - R$ {prod.preco:.2f}")
        print(f"   Ingredientes: {prod.descricao}")
    print("--------------------\n")


# Realizar busca de cliente por CPF para participar do desconto de fidelidade
def buscar_cliente(cpf):
    for c in clientes:
        if c.cpf == cpf:
            return c
    return None


# Cadastro de clientes para desconto de fidelidade
def cadastrar_cliente():
    print("\n    Cadastro Clube Xêro da Tia    ")
    cpf = input("Digite seu CPF (apenas números): ")

    # Evitar cadastro em duplicidade
    if buscar_cliente(cpf) is not None:
        print("Este CPF já está cadastrado \n")
        return

    nome = input("Digite seu nome: ")
    telefone = input("Digite seu telefone: ")

    novo_cliente = Cliente(cpf, nome, telefone)
    clientes.append(novo_cliente)
    print(f"{nome} cadastrado com sucesso! \nBem vindo(a) ao Clube Xêro da Tia")
    print("A cada 10 itens comprados a Tia tem uma surpresa especial para você! \n")


# Iniciar pedido
def realizar_pedido():
    print("    Anotando Pedido    ")
    # Verificar se faz parte do clube
    print("Digite seu CPF caso seja membro do Clube Xêro da Tia, se não for deixe em branco o campo")
    cpf = input("CPF: ")
    cliente_atual = buscar_cliente(cpf) if cpf else None

    if cliente_atual:
        print(
            f"Cliente identificado: {cliente_atual.nome} | Saldo em pontos: "
            f"{cliente_atual.pontos}/10"
        )
        nome_cliente_registro = cliente_atual.nome
    else:
        print("Cliente não fidelizado \n")
        nome_cliente_registro = "Cliente"

    exibir_cardapio()
    if not cardapio:
        print("Cardápio não foi carregado, tente novamente mais tarde")
        return

    itens_pedido = []
    subtotal = 0.0

    while True:
        try:
            cod = int(input("\nDigite o código do produto (pressione 0 para finalizar o pedido): "))
            if cod == 0:
                break

            produto_encontrado = None
            for p in cardapio:
                if p.codigo == cod:
                    produto_encontrado = p
                    break

            # Bloco recuado para fora do loop 'for'
            if produto_encontrado:
                itens_pedido.append(produto_encontrado)
                subtotal += produto_encontrado.preco
                print(f"{produto_encontrado.nome} adicionado!")
            else:
                print("Código de produto inválido \n")
        except ValueError:
            print("Código de produto inválido \n")

    qtd_itens = len(itens_pedido)

    if qtd_itens > 0:
        desconto = 0.0

        if cliente_atual:
            cliente_atual.pontos += qtd_itens
            print(f"\nPontos acumulados nesta compra: +{qtd_itens}")

            if cliente_atual.pontos >= 10:
                desconto = 5.00
                cliente_atual.pontos -= 10
                print("Você atigiu 10 pontos e a Tia Rosa mandou um agrado. \n")
                print("Geramos um desconto de R$ 5,00 na sua compra! \n")
                print(f"Pontos para o próximo resgate: {cliente_atual.pontos}/10")
            else:
                print(f"Saldo atual: {cliente_atual.pontos}/10 pontos para o próximo resgate")

        total_final = subtotal - desconto 

        print(f"\nSubtotal: R$ {subtotal:.2f}")

        if desconto > 0:
            print(f"Desconto Aplicado: -R$ {desconto:.2f}")
        print(f"Valor Total Final: R$ {total_final:.2f}")

        # Enviar para arquivo de registro de vendas
        gravar_venda(nome_cliente_registro, itens_pedido, total_final, desconto)

        print("Pedido finalizado e registrado em nosso sistema \n")
        print("Sua comida já está sendo preparada \n")
    else:
        print("Pedido cancelado (nenhum item selecionado). \n")


# Criação do Menu
def menu():
    while True:
        print("\n===============================")
        print("    COFFEE SHOPS TIA ROSA    ")
        print("=============================== \n")
        print("1. Ver Cardápio detalhado")
        print("2. Fazer Pedido")
        print("3. Cadastrar Cliente (Clube Xêro da Tia)")
        print("4. Ver Relatório de Vendas")
        print("5. Sair \n")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exibir_cardapio()
        elif opcao == "2":
            realizar_pedido()
        elif opcao == "3":
            cadastrar_cliente()
        elif opcao == "4":
            relatorio_vendas()
        elif opcao == "5":
            print("Encerrando sistema. \n")
            break
        else:
            print("Opção inválida. \n")


if __name__ == "__main__":
    menu()