import os
import subprocess


class LinuxAssistant:
    """Classe utilitária para interações simples do sistema."""

    @staticmethod
    def list_directory(path: str = ".") -> str:
        try:
            items = os.listdir(path)
            return "\n".join(items) if items else "Diretório vazio."
        except FileNotFoundError:
            return f"Caminho não encontrado: {path}"

    @staticmethod
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

    @staticmethod
    def get_system_status() -> str:
        status = []
        try:
            uname = subprocess.run(["uname", "-a"], capture_output=True, text=True, check=False)
            status.append("Sistema:")
            status.append(uname.stdout.strip() or "Não foi possível obter informações do sistema.")
        except Exception:
            pass

        try:
            df = subprocess.run(["df", "-h"], capture_output=True, text=True, check=False)
            status.append("\nUso de disco:\n" + (df.stdout.strip() or "Não foi possível obter o uso de disco."))
        except Exception:
            pass

        try:
            free = subprocess.run(["free", "-m"], capture_output=True, text=True, check=False)
            status.append("\nMemória:\n" + (free.stdout.strip() or "Não foi possível obter a memória."))
        except Exception:
            pass

        return "\n".join(status)
