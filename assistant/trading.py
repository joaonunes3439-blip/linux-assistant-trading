import subprocess


DEFAULT_MODEL = "llama3.2"


def _list_ollama_models() -> list[str]:
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            return []

        lines = result.stdout.strip().splitlines()
        models = []
        for line in lines[1:]:
            parts = line.split()
            if parts:
                models.append(parts[0])
        return models
    except FileNotFoundError:
        return []


def _fallback_response(prompt: str) -> str:
    lower = prompt.lower()

    if "btc" in lower or "bitcoin" in lower:
        return "Posso consultar o BTC. Tente: 'preço do BTC'."
    if "petr4" in lower or "petrobras" in lower:
        return "Posso consultar a PETR4. Tente: 'sinal da PETR4'."
    if "status" in lower:
        return "Para ver o status do sistema, digite: 'status'."
    if "listar" in lower or "ls" in lower:
        return "Para listar arquivos, digite: 'listar .' ou 'lista /tmp'."

    return "Posso ajudar com status do sistema, comandos do Linux e mercado financeiro. Tente: 'status', 'listar /tmp', 'preço do BTC' ou 'sinal da PETR4'."


def generate_reply(prompt: str) -> str:
    models = _list_ollama_models()
    if not models:
        return _fallback_response(prompt)

    model = models[0]
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass

    return _fallback_response(prompt)
