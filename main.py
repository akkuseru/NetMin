import os
from core.checks import run_full_check
from ui.menu import show_main_menu
from ui.banner import print_banner
from rich.console import Console

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print_banner()

    console = Console()
    console.print("\n[cyan]Comprobando entorno...[/cyan]")
    full_mode = run_full_check()

    if full_mode:
        console.print("[green]✔ Todo listo. Iniciando NetMin.[/green]")
    else:
        console.print("[yellow]⚠ Modo degradado: Algunas funciones estarán limitadas.[/yellow]")

    input("\nPresiona Enter para continuar...")  # Pausa antes de limpiar
    clear_screen()
    show_main_menu(degraded_mode=not full_mode)

if __name__ == "__main__":
    main()
