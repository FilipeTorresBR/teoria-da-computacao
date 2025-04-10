class AFND:
    def __init__(self, alfabeto, estados, transicoes, estado_inicial, estados_finais):
        self.alfabeto = alfabeto
        self.estados = estados
        self.transicoes = transicoes  # formato: {(estado, simbolo): [estados_destino]}
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def eh_deterministico(self):
        #Verifica se o autômato é determinístico
        for estado in self.estados:
            for simbolo in self.alfabeto:
                destinos = self.transicoes.get((estado, simbolo), [])
                if len(destinos) > 1:
                    return False
                if simbolo == 'e' and destinos:  # epsilon transições tornam não determinístico
                    return False
        return True

    def fecho_epsilon(self, estados):
        #Calcula o fecho-e para um conjunto de estados
        fecho = set(estados)
        pilha = list(estados)
        
        while pilha:
            estado = pilha.pop()
            destinos = self.transicoes.get((estado, 'e'), [])
            for destino in destinos:
                if destino not in fecho:
                    fecho.add(destino)
                    pilha.append(destino)
        return fecho

    def converter_para_afd(self):
        #Converte o AFND para AFD usando construção de subconjuntos
        print("\nIniciando conversão de AFND para AFD...")
        
        # Novo estado inicial é o fecho-e do estado inicial original
        novo_inicial = frozenset(self.fecho_epsilon([self.estado_inicial]))
        estados_afd = [novo_inicial]
        transicoes_afd = {}
        estados_finais_afd = []
        
        # Verifica se o novo estado inicial contém algum estado final
        if any(estado in self.estados_finais for estado in novo_inicial):
            estados_finais_afd.append(novo_inicial)
        
        fila = [novo_inicial]
        processados = set()
        
        while fila:
            conjunto_atual = fila.pop(0)
            if conjunto_atual in processados:
                continue
            processados.add(conjunto_atual)
            
            for simbolo in self.alfabeto:
                if simbolo == 'e':
                    continue
                
                # Calcula o conjunto de estados alcançáveis
                destinos = set()
                for estado in conjunto_atual:
                    destinos.update(self.transicoes.get((estado, simbolo), []))
                
                if not destinos:
                    continue
                
                # Calcula o fecho-e dos destinos
                novo_conjunto = frozenset(self.fecho_epsilon(destinos))
                
                # Adiciona a transição
                transicoes_afd[(conjunto_atual, simbolo)] = novo_conjunto
                
                # Se o novo conjunto não foi processado, adiciona à fila
                if novo_conjunto not in estados_afd:
                    estados_afd.append(novo_conjunto)
                    fila.append(novo_conjunto)
                
                # Verifica se é estado final
                if any(estado in self.estados_finais for estado in novo_conjunto):
                    if novo_conjunto not in estados_finais_afd:
                        estados_finais_afd.append(novo_conjunto)
        
        # Mapeia os conjuntos para nomes mais legíveis (q0, q1, etc.)
        mapeamento = {conjunto: f'q{i}' for i, conjunto in enumerate(estados_afd)}
        
        # Converte as transições e estados para os novos nomes
        novas_transicoes = {}
        for (conjunto, simbolo), destino in transicoes_afd.items():
            novas_transicoes[(mapeamento[conjunto], simbolo)] = mapeamento[destino]
        
        novos_estados = [mapeamento[conjunto] for conjunto in estados_afd]
        novo_estado_inicial = mapeamento[novo_inicial]
        novos_estados_finais = [mapeamento[conjunto] for conjunto in estados_finais_afd]
        
        print("\nConversão concluída com sucesso!")
        print(f"Estados do AFD: {novos_estados}")
        print(f"Estado inicial: {novo_estado_inicial}")
        print(f"Estados finais: {novos_estados_finais}")
        print("Transições:")
        for (origem, simbolo), destino in novas_transicoes.items():
            print(f"  {origem} --{simbolo}--> {destino}")
        
        return AFD(self.alfabeto, novos_estados, novas_transicoes, novo_estado_inicial, novos_estados_finais)


class AFD:
    def __init__(self, alfabeto, estados, transicoes, estado_inicial, estados_finais):
        self.alfabeto = alfabeto
        self.estados = estados
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def eh_deterministico(self):
        #Verifica se o AFD é determinístico
        for estado in self.estados:
            for simbolo in self.alfabeto:
                # Verifica se há mais de uma transição definida para o mesmo estado e símbolo
                if list(self.transicoes.keys()).count((estado, simbolo)) > 1:
                    return False
        return True

    def eh_total(self):
        #Verifica se a função de transição é total
        for estado in self.estados:
            for simbolo in self.alfabeto:
                if (estado, simbolo) not in self.transicoes:
                    return False
        return True

    def adicionar_estado_artificial(self):
        #Adiciona um estado artificial para completar transições faltantes
        estado_artificial = 'A'
        if estado_artificial not in self.estados:
            self.estados.append(estado_artificial)
        for estado in self.estados:
            for simbolo in self.alfabeto:
                if (estado, simbolo) not in self.transicoes:
                    self.transicoes[(estado, simbolo)] = estado_artificial
        print(f"Estado artificial '{estado_artificial}' adicionado para completar a função de transição.")

    def estados_alcancaveis(self):
        #Verifica se todos os estados são alcançáveis a partir do estado inicial
        alcancaveis = set()
        self._dfs(self.estado_inicial, alcancaveis)
        return alcancaveis == set(self.estados)

    def _dfs(self, estado, alcancaveis):
        #Função auxiliar para busca em profundidade
        alcancaveis.add(estado)
        for simbolo in self.alfabeto:
            proximo_estado = self.transicoes.get((estado, simbolo))
            if proximo_estado and proximo_estado not in alcancaveis:
                self._dfs(proximo_estado, alcancaveis)

    def minimizar(self):
        #Executa o algoritmo de minimização do AFD
        print("\nIniciando processo de minimização...")

        # Verifica condições necessárias
        if not self.eh_deterministico():
            return "O autômato não é determinístico. Minimização não pode ser realizada."
        if not self.eh_total():
            print("Função de transição não é total. Adicionando estado artificial...")
            self.adicionar_estado_artificial()
        if not self.estados_alcancaveis():
            return "Nem todos os estados são alcançáveis. Minimização não pode ser realizada."

        n = len(self.estados)
        tabela = [[False] * n for _ in range(n)]
        index_map = {self.estados[i]: i for i in range(n)}

        # Passo 1: Marcar pares não equivalentes
        print("\nPasso 1: Marcando pares de estados trivialmente não equivalentes...")
        for i in range(n):
            for j in range(i):
                estado1, estado2 = self.estados[i], self.estados[j]
                if (estado1 in self.estados_finais) != (estado2 in self.estados_finais):
                    tabela[i][j] = True
                    print(f"Marcados como não equivalentes: ({estado1}, {estado2})")

        # Passo 2: Analisar os pares restantes
        print("\nPasso 2: Analisando pares restantes...")
        mudou = True
        while mudou:
            mudou = False
            for i in range(n):
                for j in range(i):
                    if tabela[i][j]:
                        continue
                    for simbolo in self.alfabeto:
                        proximo1 = self.transicoes.get((self.estados[i], simbolo))
                        proximo2 = self.transicoes.get((self.estados[j], simbolo))
                        if proximo1 and proximo2:
                            if tabela[index_map[proximo1]][index_map[proximo2]]:
                                tabela[i][j] = True
                                mudou = True
                                print(f"Marcados como não equivalentes: ({self.estados[i]}, {self.estados[j]}) com símbolo '{simbolo}'")
                                break

        # Passo 3: Unificação de estados equivalentes
        print("\nPasso 3: Unificando estados equivalentes...")
        novos_estados = set(self.estados)
        unificacao = {}
        for i in range(n):
            for j in range(i):
                if not tabela[i][j]:
                    unificacao[self.estados[i]] = self.estados[j]
                    novos_estados.discard(self.estados[i])
                    print(f"Unificando: {self.estados[i]} -> {self.estados[j]}")

        # Passo 4: Nova função de transição
        print("\nPasso 4: Gerando nova função de transição...")
        novas_transicoes = {}
        for (estado, simbolo), proximo_estado in self.transicoes.items():
            novo_estado = unificacao.get(estado, estado)
            novo_proximo_estado = unificacao.get(proximo_estado, proximo_estado)
            novas_transicoes[(novo_estado, simbolo)] = novo_proximo_estado

        self.estados = list(novos_estados)
        self.transicoes = novas_transicoes
        self.estados_finais = [unificacao.get(estado, estado) for estado in self.estados_finais if estado in novos_estados]

        print("\nAFD minimizado com sucesso!")
        return tabela

    def validar_palavra(self, palavra_entrada):
        #Valida uma palavra no AFD minimizado
        estado_atual = self.estado_inicial
        print(f"\nValidando a palavra '{palavra_entrada}':")
        for simbolo in palavra_entrada:
            if simbolo not in self.alfabeto:
                print(f"Erro: Símbolo '{simbolo}' não pertence ao alfabeto.")
                return False
            proximo_estado = self.transicoes.get((estado_atual, simbolo))
            if not proximo_estado:
                print(f"Erro: Não há transição do estado '{estado_atual}' com '{simbolo}'.")
                return False
            print(f"Transição: {estado_atual} --({simbolo})--> {proximo_estado}")
            estado_atual = proximo_estado
        if estado_atual in self.estados_finais:
            print(f"A palavra foi aceita. Estado final: {estado_atual}")
            return True
        else:
            print(f"A palavra foi rejeitada. Estado final: {estado_atual} (não é estado final)")
            return False


def imprimir_tabela(tabela, estados):
    #Imprime a tabela de pares de estados
    print("\nTabela de Pares de Estados Possíveis:")
    n = len(estados)
    print("   " + "  ".join(estados))
    for i in range(n):
        linha = f"{estados[i]} "
        for j in range(i):
            linha += " T " if tabela[i][j] else " F "
        print(linha)


def criar_afnd():
    #Cria um AFND a partir da entrada do usuário
    alfabeto = input("Digite o alfabeto (símbolos separados por espaço, use 'e' para epsilon): ").split()
    estados = input("Digite os estados (separados por espaço): ").split()
    estado_inicial = input("Digite o estado inicial: ")
    estados_finais = input("Digite os estados finais (separados por espaço): ").split()
    transicoes = {}
    print("Defina as transições (no formato 'estado atual símbolo estados seguintes'):")
    print("Exemplo: q0 a q1 q2 (para transições não determinísticas)")
    print("Para epsilon transições, use e como símbolo")
    
    while True:
        entrada = input("Transição (ou 'done' para finalizar): ")
        if entrada == "done":
            break
        partes = entrada.split()
        estado_atual = partes[0]
        simbolo = partes[1]
        estados_destino = partes[2:]
        transicoes[(estado_atual, simbolo)] = estados_destino
    
    return AFND(alfabeto, estados, transicoes, estado_inicial, estados_finais)


def criar_afd():
    #Cria um AFD a partir da entrada do usuário
    alfabeto = input("Digite o alfabeto (símbolos separados por espaço): ").split()
    estados = input("Digite os estados (separados por espaço): ").split()
    estado_inicial = input("Digite o estado inicial: ")
    estados_finais = input("Digite os estados finais (separados por espaço): ").split()
    transicoes = {}
    print("Defina as transições (no formato 'estado atual símbolo estado seguinte'):")
    
    while True:
        entrada = input("Transição (ou 'done' para finalizar): ")
        if entrada == "done":
            break
        estado_atual, simbolo, proximo_estado = entrada.split()
        transicoes[(estado_atual, simbolo)] = proximo_estado
    
    return AFD(alfabeto, estados, transicoes, estado_inicial, estados_finais)


def main():
    print("Escolha o tipo de autômato:")
    print("1 - Autômato Finito Determinístico (AFD)")
    print("2 - Autômato Finito Não Determinístico (AFND)")
    opcao = input("Opção: ")
    
    if opcao == "1":
        afd = criar_afd()
    elif opcao == "2":
        afnd = criar_afnd()
        print("\nAutômato Finito Não Determinístico criado:")
        print(f"Estados: {afnd.estados}")
        print(f"Estado inicial: {afnd.estado_inicial}")
        print(f"Estados finais: {afnd.estados_finais}")
        print("Transições:")
        for (origem, simbolo), destinos in afnd.transicoes.items():
            print(f"  {origem} --{simbolo}--> {', '.join(destinos)}")
        
        print("\nConvertendo AFND para AFD...")
        afd = afnd.converter_para_afd()
    else:
        print("Opção inválida.")
        return
    
    # Agora trabalhamos com o AFD (original ou convertido)
    tabela = afd.minimizar()
    if isinstance(tabela, str):
        print(tabela)
    else:
        imprimir_tabela(tabela, afd.estados)
    
    while True:
        palavra = input("Digite uma palavra para testar (ou 'sair' para finalizar): ")
        if palavra == "sair":
            break
        afd.validar_palavra(palavra)


if __name__ == "__main__":
    main()
