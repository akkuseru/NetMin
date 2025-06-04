from rich.console import Console
from rich.prompt import Prompt

console = Console()

def choose_scan_range(ip, network):
    console.print(f"Subred detectada: [cyan]{network}[/cyan]")
    console.print(f"IP local: [green]{ip}[/green]\n")

    options = {
        "1": f"Escanear toda la subred {network}",
        "2": f"Escanear solo la IP local {ip}",
        "3": "Cancelar"
    }
    for key, desc in options.items():
        console.print(f"{key}. {desc}")

    choice = Prompt.ask("¿Qué quieres escanear?", choices=options.keys())

    if choice == "1":
        return network
    elif choice == "2":
        return ip
    else:
        return None
