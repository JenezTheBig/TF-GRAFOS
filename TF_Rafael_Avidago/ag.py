import networkx as nx
import random
import numpy as np

# Função para criar um grafo com pesos aleatórios nas arestas
def criar_grafo(num_nos):
    G = nx.complete_graph(num_nos)
    for (u, v) in G.edges():
        G.edges[u, v]['peso'] = random.randint(1, 10)
    return G

# Função objetivo: calcula o custo total do caminho
def calcular_custo(G, caminho):
    custo = 0
    for i in range(len(caminho)):
        if i == len(caminho) - 1:
            custo += G[caminho[i]][caminho[0]]['peso']
        else:
            custo += G[caminho[i]][caminho[i + 1]]['peso']
    return custo

# Operador de cruzamento OX
def cruzamento_ox(pai1, pai2):
    tamanho = len(pai1)
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    filho1, filho2 = [None] * tamanho, [None] * tamanho
    filho1[inicio:fim + 1], filho2[inicio:fim + 1] = pai1[inicio:fim + 1], pai2[inicio:fim + 1]

    def preencher_filho(filho, pai):
        pos_atual = fim + 1
        for no in pai:
            if no not in filho:
                if pos_atual >= tamanho:
                    pos_atual = 0
                filho[pos_atual] = no
                pos_atual += 1

    preencher_filho(filho1, pai2)
    preencher_filho(filho2, pai1)
    return filho1, filho2

# Inicialização da população
def inicializar_populacao(num_individuos, num_nos):
    return [np.random.permutation(num_nos) for _ in range(num_individuos)]

# Seleção por torneio
def selecao_torneio(populacao, G, tamanho_torneio):
    selecionados = []
    for _ in range(len(populacao)):
        torneio = random.sample(populacao, tamanho_torneio)
        melhor = min(torneio, key=lambda ind: calcular_custo(G, ind))
        selecionados.append(melhor)
    return selecionados

# Mutação: troca dois nós de posição
def mutacao(individuo):
    idx1, idx2 = random.sample(range(len(individuo)), 2)
    individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo

# Função para calcular a diversidade da população
def calcular_diversidade(populacao):
    diversidade = 0
    num_individuos = len(populacao)
    for i in range(num_individuos):
        for j in range(i + 1, num_individuos):
            distancia = sum(p1 != p2 for p1, p2 in zip(populacao[i], populacao[j]))
            diversidade += distancia
    return diversidade / (num_individuos * (num_individuos - 1) / 2) if num_individuos > 1 else 0

# Algoritmo genético
def algoritmo_genetico(G, num_geracoes, tamanho_populacao, tamanho_torneio, taxa_cruzamento, taxa_mutacao, limite_estagnacao, limiar_diversidade):
    populacao = inicializar_populacao(tamanho_populacao, len(G.nodes))
    melhor_solucao, melhor_custo = None, float('inf')
    contador_estagnacao, diversidade_atual = 0, float('inf')

    for geracao in range(num_geracoes):
        print(f"Geracao: {geracao + 1}")
        selecionados = selecao_torneio(populacao, G, tamanho_torneio)
        descendentes = []
        for i in range(0, len(selecionados), 2):
            if random.random() < taxa_cruzamento and i + 1 < len(selecionados):
                desc1, desc2 = cruzamento_ox(selecionados[i], selecionados[i+1])
                descendentes.extend([desc1, desc2])
            else:
                descendentes.append(selecionados[i])
                if i + 1 < len(selecionados):
                    descendentes.append(selecionados[i + 1])

        for ind in descendentes:
            if random.random() < taxa_mutacao:
                mutacao(ind)

        populacao = descendentes
        print("Rotas feitas nessa geracao:")
        for route in populacao:
            print(route)
        custo_atual_melhor = float('inf')
        for ind in populacao:
            custo = calcular_custo(G, ind)
            if custo < custo_atual_melhor:
                custo_atual_melhor = custo
            if custo < melhor_custo:
                melhor_custo, melhor_solucao = custo, ind

        print(f"Melhor custo nessa geracao: {custo_atual_melhor}")

        diversidade_atual = calcular_diversidade(populacao)

        if diversidade_atual < limiar_diversidade:
            # Introduzir novos indivíduos ou aumentar a taxa de mutação
            populacao.extend(inicializar_populacao(int(tamanho_populacao * 0.1), len(G.nodes)))
            taxa_mutacao *= 1.5  # Aumenta a taxa de mutação

        if custo_atual_melhor >= melhor_custo:
            contador_estagnacao += 1
        else:
            contador_estagnacao = 0

        if contador_estagnacao >= limite_estagnacao:
            break

    return melhor_solucao, melhor_custo

# Função principal
def main():
    num_cidades = int(input("Informe o número de cidades: "))
    G = criar_grafo(num_cidades)

    num_geracoes = 100
    tamanho_populacao = int(input("Informe o tamanho da população: "))
    tamanho_torneio = 5
    taxa_cruzamento = float(input("Informe a taxa de cruzamento (0 a 1): "))
    taxa_mutacao = float(input("Informe a taxa de mutação (0 a 1): "))
    limite_estagnacao = 10
    limiar_diversidade = 0.1

    melhor_caminho, custo_melhor_caminho = algoritmo_genetico(G, num_geracoes, tamanho_populacao, tamanho_torneio, taxa_cruzamento, taxa_mutacao, limite_estagnacao, limiar_diversidade)
    print("Melhor caminho:", melhor_caminho, "com custo:", custo_melhor_caminho)

if __name__ == "__main__":
    main()
