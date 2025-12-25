
# ENUNCIADO DO PROJETO FINAL

## Título

`expcli`: Interface de Linha de Comando para Análise de Experiências Comportamentais

## Contexto

Imagina que o teu laboratório corre regularmente pequenas experiências comportamentais (por exemplo, tarefas de tempo de reação, escolha entre opções, etc.). Os dados são guardados em ficheiros CSV e já existe um módulo Python que:

* lê esses dados,
* faz validação básica,
* calcula estatísticas descritivas simples,
* gera pequenos relatórios de resultados.

**O problema**: este módulo só pode ser usado diretamente em Python, o que torna o fluxo de trabalho menos acessível para pessoas que não programam.

O objetivo é criar uma **ferramenta de linha de comando (CLI)** em Python, que envolva esse módulo e permita que qualquer pessoa no laboratório use as funcionalidades de análise diretamente no terminal, sem escrever código Python.

## Material fornecido

* Uma pequena pasta `examples/` com 4 ficheiros CSV de exemplo;

* um módulo Python (`expstats.py`) com a seguinte API:

```python
# expstats.py (exemplo de interface)

def load_session(csv_path: str) -> dict:
    """Lê um ficheiro CSV de sessão e devolve um dicionário com os dados e metadados."""

def list_participants(data_dir: str) -> list[str]:
    """Devolve a lista de IDs de participantes encontrados nos CSVs de um diretório."""

def compute_summary(csv_path: str) -> dict:
    """
    Calcula estatísticas descritivas (médias, desvios padrão, número de trials válidos,
    percentagem de erros, etc.) para uma sessão.
    """

def compare_groups(csv_paths_a: list[str], csv_paths_b: list[str]) -> dict:
    """
    Compara duas condições (A e B) e devolve métricas agregadas (diferença de tempos de reação,
    diferença de percentagens de erro, etc.).
    """

def generate_report(summary: dict, out_path: str) -> None:
    """Gera um relatório de texto simples a partir de um dicionário de resultados."""
```

* Este módulo é considerado **“caixa fechada”**: não pode ser alterado.
* O objetivo é construir uma **CLI robusta e bem desenhada** que use estas funções.

(Nota: a interface exata das funções está documentada no ficheiro fornecido, o ficheiro n~ao pode ser alterado mas pode ser consultado!)

## Objetivo geral

Desenvolver um programa de linha de comando em Python que:

1. Use o módulo fornecido para carregar e analisar dados de experiências.
2. Disponibilize comandos claros para as operações mais comuns (listar participantes, obter resumos, comparar condições, gerar relatórios).
3. Seja utilizável apenas a partir do terminal, com uma interface coerente, mensagens de ajuda claras e tratamento de erros cuidado.

## Requisitos funcionais

O programa deverá ser chamado, por exemplo, `expcli.py` e suportar pelo menos os seguintes comandos:

### 1. Comando `list-participants`

_Uso_:

  ```bash
  python expcli.py list-participants --data-dir <pasta_dados>
  ```

_Comportamento_:

* Lista todos os IDs de participantes encontrados na pasta indicada (por exemplo, com base nos nomes dos ficheiros).
* Ordena alfabeticamente os IDs.
* Se a pasta não existir ou estiver vazia, apresenta uma mensagem de erro clara.

### 2. Comando `summary`

_Uso_:

  ```bash
  python expcli.py summary --file <ficheiro.csv>
  ```

_Comportamento_:

* Usa `compute_summary` para calcular estatísticas dessa sessão.
* Imprime no ecrã um resumo legível, por exemplo:

    ```bash
    Participante: P001
    Condição: A
    Trials válidos: 120
    Tempo de reação médio: 350.4 ms
    Erros: 8 (6.7%)
    ...
    ```

Deve tratar:

* Ficheiro inexistente (mensagem de erro útil).
* Ficheiro com formato inválido (usar as exceções do módulo e traduzir em mensagens amigáveis).

### 3. Comando `compare-groups`

_Uso_ (exemplo 1: com padrões de ficheiros):

  ```bash
  python expcli.py compare-groups \
      --group-a "data/condA_*.csv" \
      --group-b "data/condB_*.csv"
  ```

_Uso_ (exemplo 2: com múltiplas opções):

  ```bash
  python expcli.py compare-groups \
      --group-a data/A_P001.csv data/A_P002.csv \
      --group-b data/B_P001.csv data/B_P002.csv
  ```

_Comportamento_:

* Usa `compare_groups` para obter métricas agregadas entre dois grupos.
* Apresenta um resumo comparativo, por exemplo:

    ```bash
    Grupo A: 20 sessões, TR médio = 340.2 ms, erros = 5.1%
    Grupo B: 22 sessões, TR médio = 365.8 ms, erros = 7.4%

    Diferença TR (B - A): +25.6 ms
    Diferença erros (B - A): +2.3 pontos percentuais
    ```

Deve validar:

* Se existirem ficheiros para ambos os grupos.
* Se algum ficheiro estiver corrompido/ilegível (deve indicar qual e continuar de forma sensata, ou abortar com mensagem clara, como ficar definido na documentação).

### 4. Comando `report`

_Uso_:

  ```bash
  python expcli.py report --file <ficheiro.csv> --out <relatorio.txt>
  ```

_Comportamento_:

Usa `compute_summary` e `generate_report` para gerar um relatório e guardá-lo em disco.
Se o ficheiro de saída já existir:

* Por omissão, pergunta interativamente se deve sobrescrever (Y/N).
* OU, em alternativa, só sobrescreve se for passado um argumento `--force`.

### 5. Opções globais

Todos os comandos devem suportar:

* `-h` / `--help`: mostra ajuda geral e/ou ajuda específica de cada comando.
* `-v` / `--verbose`: modo detalhado, em que são mostradas mensagens sobre o que o programa está a fazer (ficheiros lidos, número de sessões encontradas, etc.).
* `--version`: mostra a versão do programa (por exemplo, `expcli 1.0`).

Sugestão (não obrigatório, mas recomendado): usar o módulo `argparse` com subcomandos.

## Requisitos não funcionais

1. **Estrutura do código**

    O código deve estar organizado de forma modular, por exemplo:

    * `expcli.py` (script principal com `if __name__ == "__main__":`)
    * `cli.py` (funções relacionadas com parsing de argumentos e dispatch dos comandos)
    * `utils.py` (eventuais funções auxiliares)
    * O módulo fornecido (`expstats.py`) não deve ser modificado.  

    **NB**: Este é um exemplo, pode ser entregue também apenas um ficheiro com tudo.

2. **Tratamento de erros**

   O programa não deverá “rebentar” com tracebacks default em situações razoáveis de erro
   do utilizador (pasta errada, ficheiro em falta, etc.).
   Em caso de erro, deve:

    * Imprimir uma mensagem clara e curta.
    * Terminar com um código de saída diferente de 0 (por exemplo, `sys.exit(1)`).

3. **Documentação para o utilizador**

   Ficheiro `README.md` com:

    * Descrição breve do objetivo do programa.
    * Requisitos (versão de Python, módulos necessários).
    * Instruções de instalação/execução.
    * Exemplos de utilização de cada comando.

4. **Legibilidade e estilo**

    * Código organizado, com nomes de variáveis e funções significativos.
    * Comentários curtos onde necessário.
    * Seguir, tanto quanto possível, o estilo PEP 8.

## Extensões opcionais (para nota extra)

Estas extensões não são obrigatórias, mas podem contribuir para melhorar a classificação se o resto estiver sólido:

1. **Testes básicos**

    Incluir pelo menos alguns testes simples (podem ser scripts próprios ou usar `unittest`/`pytest`) que verifiquem:

    * Que os comandos básicos funcionam sobre um pequeno conjunto de dados de exemplo.
    * Que certas situações de erro produzem mensagens/saídas adequadas.
    Explicar no `README` como correr esses testes.

2. **Modo interativo**

   * Um comando tipo `python expcli.py shell` que abre um mini-“shell” interativo onde o utilizador pode correr os comandos `list`, `summary`, `compare`, etc., sem voltar sempre ao terminal.

3. **Configuração via ficheiro**

   * Permitir um ficheiro de configuração (por exemplo, `config.toml` ou `config.ini`) onde se define o diretório de dados por omissão, parâmetros de relatório, etc.
   * Suportar uma flag `--config` para indicar o ficheiro de configuração.

4. **Exportação para JSON**

   * Permitir que os resultados dos comandos `summary` e `compare-groups` sejam exportados em formato JSON com uma opção `--json <ficheiro.json>`.

Se implementares extensões, descreve-as claramente no `README`.

## Entrega

Material para entregar:

1. Código fonte (todos os ficheiros `.py` necessários);
2. Ficheiro `README.md`;
3. Opcional: ficheiros de teste (e.g., `tests/`).

## Critérios de avaliação

* Funcionalidade e correção dos comandos (incluindo tratamento de erros).
* Qualidade da interface de linha de comando (claridade dos comandos, ajuda, mensagens).
* Organização e qualidade do código.
* Documentação e exemplos de utilização.
* Eventuais extensões bem implementadas.
