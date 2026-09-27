import os
import subprocess


def list_directory(path: str = ".") -> str:
    try:
        items = sorted(os.listdir(path))
        if not items:
            return "Diretório vazio."
        return "\n".join(items)
    except FileNotFoundError:
        return f"Caminho não encontrado: {path}"
    except OSError as exc:
        return f"Erro ao listar diretório: {exc}"


def execute_shell_command(command: str) -> str:
    if not command.strip():
        return "Comando vazio."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
        output = result.stdout.strip() or result.stderr.strip() or "Comando executado sem saída."
        return output
    except subprocess.TimeoutExpired:
        return "Comando excedeu o tempo limite."
    except Exception as exc:
        return f"Erro ao executar comando: {exc}"


def get_system_status() -> str:
    blocks = []

    uname = subprocess.run(["uname", "-a"], capture_output=True, text=True, check=False)
    blocks.append("Sistema:")
    blocks.append(uname.stdout.strip() or "Não foi possível obter informações do sistema.")

    df = subprocess.run(["df", "-h"], capture_output=True, text=True, check=False)
    blocks.append("\nUso de disco:\n" + (df.stdout.strip() or "Não foi possível obter o uso de disco."))

    free = subprocess.run(["free", "-m"], capture_output=True, text=True, check=False)
    blocks.append("\nMemória:\n" + (free.stdout.strip() or "Não foi possível obter a memória."))

    return "\n".join(blocks)
