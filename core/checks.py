from rich.console import Console
from rich.table import Table
from time import sleep
import platform
import subprocess
import os
import sys

console = Console()

def check_dependencies():
    results = []
    for lib in ['scapy', 'rich', 'psutil']:
        try:
            __import__(lib)
            results.append((lib, True))
        except ImportError:
            results.append((lib, False))
    return results

def check_npcap():
    system = platform.system()
    if system == "Windows":
        try:
            output = subprocess.check_output('sc query npcap', shell=True, text=True)
            return "RUNNING" in output or "STOPPED" in output
        except subprocess.CalledProcessError:
            return False
    elif system in ("Linux", "Darwin"):
        paths = ['/usr/lib/libpcap.so', '/usr/lib/x86_64-linux-gnu/libpcap.so']
        return any(os.path.exists(p) for p in paths)
    else:
        return False

def run_full_check():
    console.rule("[bold blue]Comprobando dependencias de NetScope")
    table = Table(title="Estado del sistema", show_lines=True)
    table.add_column("Dependencia", style="cyan", justify="left")
    table.add_column("Estado", style="green")

    deps_ok = True
    for lib, ok in check_dependencies():
        table.add_row(lib, "[green]✔ OK" if ok else "[red]✖ Faltante")
        if not ok:
            deps_ok = False

    # Npcap/libpcap
    npcap_ok = check_npcap()
    table.add_row("Npcap/libpcap", "[green]✔ Detectado" if npcap_ok else "[yellow]⚠ No detectado")

    console.print(table)

    if not deps_ok:
        console.print("[bold red]Faltan dependencias esenciales. Por favor instala con:[/bold red]")
        console.print("[bold yellow]pip install -r requirements.txt[/bold yellow]")
        sys.exit(1)

    if not npcap_ok:
        console.print("[bold yellow]Advertencia: No se detectó Npcap/libpcap.[/bold yellow]")
        console.print("Entrando en modo degradado...\n")
        sleep(2)
        return False  # modo degradado

    console.print("[bold green]✓ Todo en orden. Iniciando NetMin...[/bold green]")
    sleep(1)
    return True
