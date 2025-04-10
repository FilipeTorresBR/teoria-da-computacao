# Teoria dos Autômatos 

Este projeto foi desenvolvido para a disciplina de **Teoria da Computação** e tem como objetivo permitir a criação e simulação de **Autômatos Finitos Determinísticos (AFDs)** e **Autômatos Finitos Não Determinísticos (AFNDs)** por meio de uma interface no terminal.

## Sobre o Projeto

Com este programa, é possível:

- Criar autômatos determinísticos e não determinísticos a partir da entrada do usuário
- Definir alfabeto, estados, estado inicial, estados finais e transições
- Simular a leitura de palavras
- Verificar se uma palavra é aceita ou rejeitada pelo autômato

O projeto é voltado para fins **educacionais**, ajudando a compreender o funcionamento dos autômatos abordados em Teoria da Computação.

## Como executar

1. Certifique-se de ter o **Python 3** instalado.
2. Execute o programa:

```bash
python3 main.py
```

## Exemplo de uso (via terminal)

```text
1 - Autômato Finito Determinístico (AFD)
2 - Autômato Finito Não Determinístico (AFND)
Opção: 1
Digite o alfabeto (símbolos separados por espaço): 1 0
Digite os estados (separados por espaço): q1 q2 q3
Digite o estado inicial: q1
Digite os estados finais (separados por espaço): q3
Defina as transições (formato: estado símbolo próximo_estado):
Transição (ou 'done' para finalizar): q1 1 q2
Transição (ou 'done' para finalizar): q2 0 q3
Transição (ou 'done' para finalizar): done
Digite a palavra a ser testada: 10
Resultado: Aceita 
```

## Tecnologias utilizadas

- **Python 3**

## Conteúdo relacionado

- Autômatos Finitos Determinísticos (AFD)
- Autômatos Finitos Não Determinísticos (AFND)
- Transições epsilon (ε)
- Reconhecimento de linguagens formais

## Autores
Desenvolvido por 
Filipe Kaue Torres Soares, 
Joao Gomes Siqueira Neto, 
Paulo Thiago De Oliveira Tocantins, 
como parte da disciplina de **Teoria da Computação**.
