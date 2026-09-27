import re
import sys

from assistant.ai_local import generate_reply
from assistant.commands import execute_shell_command, get_system_status, list_directory
from assistant.trading import get_asset_summary, get_signal


def extract_asset(text: str) -> str | None:
    text_upper = text.upper()
    patterns = {
        "BTC": ["BTC", "BITCOIN"],
        "ETH": ["ETH", "ETHEREUM"],
        "PETR4": ["PETR4", "PETROBRAS", "PETR"],
        "VALE3": ["VALE3", "VALE"],
        "B3SA3": ["B3SA3", "B3"],
        "AAPL": ["AAPL", "APPLE"],
        "MSFT": ["MSFT", "MICROSOFT"],
    }

    for symbol, keywords in patterns.items():
        if any(keyword in text_upper for keyword in keywords):
            return symbol

    match = re.search(r"\b[A-Z]{2,5}(?:\.[A-Z]{2,4})?\b", text_upper)
    if match:
        return match.group(0)

    return None


def show_help() -> str:
    return """Comandos disponíveis:
- status
- ajuda
- listar [caminho]
- execute [comando shell]
- preço do BTC
- sinal da PETR4
- sair

Exemplos:
- listar /tmp
- execute df -h
- preço do ETH
- sinal da VALE3
"""


def handle_command(user_input: str) -> str:
    text = user_input.strip()
    if not text:
        return "Digite algo para continuar."

    lower = text.lower()

    if lower in {"sair", "exit", "quit", "parar"}:
        return "Até logo!"

    if lower in {"ajuda", "help", "?"}:
        return show_help()

    if lower in {"status", "status do sistema", "sistema"}:
        return get_system_status()

    if lower.startswith("listar ") or lower.startswith("lista "):
        path = text.split(maxsplit=1)[1].strip()
        return list_directory(path)

    if lower.startswith("execute ") or lower.startswith("executar ") or lower.startswith("comando "):
        command = text.split(maxsplit=1)[1].strip()
        return execute_shell_command(command)

    if "preço" in lower or "cotacao" in lower or "cotação" in lower or "valor" in lower:
        asset = extract_asset(text)
        if asset:
            return get_asset_summary(asset)
        return "Posso consultar ativos como BTC, ETH, PETR4, VALE3. Exemplo: preço do BTC."

    if "sinal" in lower or "analise" in lower or "análise" in lower:
        asset = extract_asset(text)
        if asset:
            return get_signal(asset)
        return "Diga o ativo, por exemplo: sinal da PETR4." 

    if lower in {"listar", "lista", "ls"}:
        return list_directory(".")

    return generate_reply(text)


def main() -> None:
    print("Assistente Linux Trading")
    print("Digite 'ajuda' para ver os comandos.")

    while True:
        try:
            user_input = input("assistente> ")
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break

        response = handle_command(user_input)
        print(response)

        if response == "Até logo!":
            break


if __name__ == "__main__":
    main()
