"""
DESAFIO FINAL - Central de Atendimento
Aluno(a): ____________________

Arquivo unico: funcoes resolvidas + menu + testes.

Para usar o programa:     python desafio_final_resolvido.py
Para rodar os testes:     python desafio_final_resolvido.py testes
"""

import sys
from collections import deque


# ---------------------------------------------------------------
# NIVEL 1 - FILA: abrir e atender chamados
# ---------------------------------------------------------------
def criar_chamado(protocolo, nome, descricao, prioridade):
    """Ja pronta: cada chamado e um dicionario."""
    return {
        "protocolo": protocolo,
        "nome": nome,
        "descricao": descricao,
        "prioridade": prioridade,      # 1 = baixa, 2 = media, 3 = alta
        "status": "pendente",
    }


def abrir_chamado(fila, todos, nome, descricao, prioridade):
    # o protocolo e o proximo numero
    protocolo = len(todos) + 1
    chamado = criar_chamado(protocolo, nome, descricao, prioridade)
    fila.append(chamado)      # fim da fila
    todos.append(chamado)     # lista com todos os chamados
    return chamado


def atender_proximo(fila, historico):
    # se nao tem ninguem na fila, devolve None
    if len(fila) == 0:
        return None
    chamado = fila.popleft()          # tira da frente (FIFO)
    chamado["status"] = "atendido"
    historico.append(chamado)         # empilha no historico
    return chamado


# ---------------------------------------------------------------
# NIVEL 2 - PILHA: desfazer o ultimo atendimento
# ---------------------------------------------------------------
def desfazer_atendimento(fila, historico):
    if len(historico) == 0:
        return None
    chamado = historico.pop()         # o ultimo atendido (LIFO)
    chamado["status"] = "pendente"
    fila.appendleft(chamado)          # volta para a FRENTE da fila
    return chamado


# ---------------------------------------------------------------
# NIVEL 3 - ORDENACAO: lista de pendentes por prioridade
# (ESSA FOI A MAIS DIFICIL, nao tenho certeza se entendi direito)
# ---------------------------------------------------------------
def ordenar_por_prioridade(chamados):
    v = list(chamados)    # copia, pra nao mexer na fila original

    # Bubble sort: compara dois vizinhos e troca se estiverem fora de ordem.
    # Quero do maior (3) para o menor (1).
    n = len(v)
    for i in range(n - 1):
        for j in range(n - 1):
            # se o da esquerda for menor ou igual ao da direita, troca
            # (usei <= porque a dica falou de < ou <=, acho que assim
            #  os iguais tambem ficam "arrumados"?)
            if v[j]["prioridade"] <= v[j + 1]["prioridade"]:
                temp = v[j]
                v[j] = v[j + 1]
                v[j + 1] = temp
    return v


# ---------------------------------------------------------------
# NIVEL 4 - BUSCA BINARIA e RECURSAO
# ---------------------------------------------------------------
def buscar_protocolo(todos, protocolo):
    inicio = 0
    fim = len(todos) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        if todos[meio]["protocolo"] == protocolo:
            return todos[meio]
        elif todos[meio]["protocolo"] < protocolo:
            inicio = meio + 1         # procura na metade da direita
        else:
            fim = meio - 1            # procura na metade da esquerda
    return None


def contar_por_prioridade(chamados, prioridade, i=0):
    # caso base: acabou a lista
    if i >= len(chamados):
        return 0
    # passo recursivo
    if chamados[i]["prioridade"] == prioridade:
        return 1 + contar_por_prioridade(chamados, prioridade, i + 1)
    else:
        return 0 + contar_por_prioridade(chamados, prioridade, i + 1)


# ---------------------------------------------------------------
# INTERFACE (menu) - ja vinha pronta
# ---------------------------------------------------------------
def ler_inteiro(mensagem, minimo, maximo):
    while True:
        texto = input(mensagem)
        if texto.isdigit() and minimo <= int(texto) <= maximo:
            return int(texto)
        print(f"Digite um numero entre {minimo} e {maximo}.")


def mostrar(chamado):
    print(f"#{chamado['protocolo']:03d} | prioridade {chamado['prioridade']} | "
          f"{chamado['nome']}: {chamado['descricao']} [{chamado['status']}]")


def menu():
    fila, todos, historico = deque(), [], []
    while True:
        print("\n=== CENTRAL DE ATENDIMENTO ===")
        print("1) Abrir chamado")
        print("2) Atender proximo")
        print("3) Desfazer ultimo atendimento")
        print("4) Listar pendentes por prioridade")
        print("5) Buscar por protocolo")
        print("6) Relatorio")
        print("0) Sair")
        op = ler_inteiro("Escolha: ", 0, 6)

        if op == 0:
            print("Ate a proxima!")
            break
        elif op == 1:
            nome = input("Nome: ")
            desc = input("Descricao: ")
            prio = ler_inteiro("Prioridade (1-3): ", 1, 3)
            mostrar(abrir_chamado(fila, todos, nome, desc, prio))
        elif op == 2:
            c = atender_proximo(fila, historico)
            print("Atendendo:" if c else "Fila vazia.")
            if c:
                mostrar(c)
        elif op == 3:
            c = desfazer_atendimento(fila, historico)
            print("Devolvido a fila:" if c else "Nada para desfazer.")
            if c:
                mostrar(c)
        elif op == 4:
            pendentes = ordenar_por_prioridade(fila)
            if not pendentes:
                print("Nenhum chamado pendente.")
            for c in pendentes:
                mostrar(c)
        elif op == 5:
            p = ler_inteiro("Protocolo: ", 1, 10**6)
            c = buscar_protocolo(todos, p)
            mostrar(c) if c else print("Protocolo nao encontrado.")
        elif op == 6:
            print(f"Total aberto: {len(todos)} | Pendentes: {len(fila)} | "
                  f"Atendidos: {len(historico)}")
            for p in (3, 2, 1):
                print(f"Prioridade {p}: {contar_por_prioridade(todos, p)}")


# ---------------------------------------------------------------
# TESTES (vieram do arquivo desafio_final_testes.py)
# ---------------------------------------------------------------
def rodar_testes():
    resultados = []

    def teste(nome):
        def decorador(func):
            try:
                func()
                resultados.append((nome, True, ""))
            except Exception as erro:
                resultados.append((nome, False, f"{type(erro).__name__}: {erro}"))
            return func
        return decorador

    def cenario():
        fila, todos, historico = deque(), [], []
        abrir_chamado(fila, todos, "Ana", "sem internet", 2)
        abrir_chamado(fila, todos, "Bruno", "tela azul", 3)
        abrir_chamado(fila, todos, "Carla", "trocar mouse", 1)
        abrir_chamado(fila, todos, "Davi", "servidor caiu", 3)
        return fila, todos, historico

    @teste("Nivel 1: abrir chamado gera protocolos 1, 2, 3...")
    def _():
        fila, todos, _h = cenario()
        assert [c["protocolo"] for c in todos] == [1, 2, 3, 4]
        assert len(fila) == 4
        assert todos[0]["status"] == "pendente"

    @teste("Nivel 1: atender segue a ordem de chegada (FIFO)")
    def _():
        fila, todos, h = cenario()
        assert atender_proximo(fila, h)["nome"] == "Ana"
        assert atender_proximo(fila, h)["nome"] == "Bruno"
        assert len(fila) == 2 and len(h) == 2
        assert todos[0]["status"] == "atendido"

    @teste("Nivel 1: atender com fila vazia devolve None")
    def _():
        assert atender_proximo(deque(), []) is None

    @teste("Nivel 2: desfazer devolve o chamado para a FRENTE da fila")
    def _():
        fila, todos, h = cenario()
        atender_proximo(fila, h)
        atender_proximo(fila, h)
        c = desfazer_atendimento(fila, h)
        assert c["nome"] == "Bruno"
        assert fila[0]["nome"] == "Bruno"
        assert c["status"] == "pendente"
        assert len(h) == 1

    @teste("Nivel 2: desfazer sem historico devolve None")
    def _():
        assert desfazer_atendimento(deque(), []) is None

    @teste("Nivel 3: ordena por prioridade (3 primeiro), estavel")
    def _():
        fila, todos, h = cenario()
        nomes = [c["nome"] for c in ordenar_por_prioridade(fila)]
        assert nomes == ["Bruno", "Davi", "Ana", "Carla"], nomes

    @teste("Nivel 3: ordenar NAO altera a fila original")
    def _():
        fila, todos, h = cenario()
        ordenar_por_prioridade(fila)
        assert [c["nome"] for c in fila] == ["Ana", "Bruno", "Carla", "Davi"]

    @teste("Nivel 4: busca binaria acha e nao acha protocolos")
    def _():
        fila, todos, h = cenario()
        assert buscar_protocolo(todos, 3)["nome"] == "Carla"
        assert buscar_protocolo(todos, 1)["nome"] == "Ana"
        assert buscar_protocolo(todos, 4)["nome"] == "Davi"
        assert buscar_protocolo(todos, 99) is None
        assert buscar_protocolo([], 1) is None

    @teste("Nivel 4: contagem recursiva por prioridade")
    def _():
        fila, todos, h = cenario()
        assert contar_por_prioridade(todos, 3) == 2
        assert contar_por_prioridade(todos, 1) == 1
        assert contar_por_prioridade([], 3) == 0

    ok = sum(1 for _, passou, _ in resultados if passou)
    print()
    for nome, passou, msg in resultados:
        print(("[OK]   " if passou else "[FALHA]"), nome,
              f"\n         {msg}" if msg else "")
    print(f"\nResultado: {ok}/{len(resultados)} testes passaram.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "testes":
        rodar_testes()
    else:
        menu()
