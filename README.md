# Linux Assistant Trading

Assistente simples para Linux, sem API key, com:
- CLI interativo em terminal
- execução de comandos do sistema
- consulta de ativos do mercado
- análise de tendência simples
- integração opcional com Ollama (IA local)

## Funcionalidades

- Status do sistema
- Listagem de diretórios
- Execução de comandos do shell
- Consulta de preço de ações/criptomoedas
- Geração de sinal simples de compra/venda/hold
- Respostas baseadas em IA local se o Ollama estiver instalado

## Requisitos

- Python 3.10+
- Linux

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Opção com IA local (Ollama)

Se você quiser usar IA local:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

## Como executar

```bash
python app.py
```

## Exemplos de uso

- `status`
- `lista /tmp`
- `preço do BTC`
- `sinal da PETR4`
- `execute df -h`
- `ajuda`

## Estrutura do projeto

```text
.
├── app.py
├── config.py
├── requirements.txt
├── assistant/
│   ├── __init__.py
│   ├── ai_local.py
│   ├── commands.py
│   ├── trading.py
│   └── utils.py
├── .gitignore
└── README.md
```

## Observação

O módulo de mercado usa dados públicos de Yahoo Finance. Não exige chave de API, mas depende de acesso à internet.
