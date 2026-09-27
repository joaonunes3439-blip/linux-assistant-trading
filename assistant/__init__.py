from assistant.ai_local import generate_reply
from assistant.commands import execute_shell_command, get_system_status, list_directory
from assistant.trading import get_asset_summary, get_signal


def run_interaction(prompt: str) -> str:
    lower = prompt.lower()

    if lower in {"status", "status do sistema"}:
        return get_system_status()

    if lower.startswith("listar ") or lower.startswith("lista "):
        path = prompt.split(maxsplit=1)[1]
        return list_directory(path)

    if lower.startswith("execute ") or lower.startswith("executar "):
        command = prompt.split(maxsplit=1)[1]
        return execute_shell_command(command)

    if "preço" in lower or "cotacao" in lower or "cotação" in lower:
        asset = prompt.replace("preço", "").replace("cotação", "").replace("cotacao", "").strip()
        if asset:
            return get_asset_summary(asset)

    if "sinal" in lower or "análise" in lower or "analise" in lower:
        asset = prompt.replace("sinal", "").replace("análise", "").replace("analise", "").strip()
        if asset:
            return get_signal(asset)

    return generate_reply(prompt)
