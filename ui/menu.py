import os
from rich.console import Console
from rich.prompt import Prompt
from scanner import arp_scanner
from scanner.network_utils import get_local_subnets_with_interfaces, detect_vpn_connections
from ui.banner import print_banner
from ui.scan_options import choose_scan_range

console = Console()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_main_menu(degraded_mode=False):
    while True:
        clear_screen()
        print_banner()
        console.print("[bold cyan]NetMin - Menú Principal[/bold cyan]")

        if degraded_mode:
            console.print("[yellow]Modo degradado activo: algunas funciones pueden estar limitadas.[/yellow]")

        console.print("1. Ver interfaces y subredes activas")
        console.print("2. Escanear dispositivos en red local")
        console.print("3. Salir")
        choice = Prompt.ask("\nElige una opción", choices=["1", "2", "3"])

        if choice == "1":
            subnets = get_local_subnets_with_interfaces()
            if not subnets:
                console.print("[red]No se detectaron subredes activas.[/red]")
            else:
                console.print("\n[green]Interfaces y subredes activas:[/green]")
                for i, (iface, ip, subnet) in enumerate(subnets, 1):
                    console.print(f"{i}. {iface}: IP {ip}, Subred {subnet}")
            input("\nPresiona Enter para continuar...")

        elif choice == "2":
            if degraded_mode:
                console.print("[red]Función no disponible en modo degradado. Requiere Npcap/libpcap.[/red]")
                input("\nPresiona Enter para continuar...")
            else:
                subnets = get_local_subnets_with_interfaces()
                if not subnets:
                    console.print("[red]No se detectaron subredes activas.[/red]")
                    input("\nPresiona Enter para continuar...")
                    continue

                # Si hay más de una subred, dejar elegir
                if len(subnets) > 1:
                    console.print("Se han detectado múltiples subredes activas:")
                    for i, (iface, ip, subnet) in enumerate(subnets, 1):
                        console.print(f"{i}. {iface}: IP {ip}, Subred {subnet}")
                    choice_iface = Prompt.ask("Selecciona la subred que quieres escanear", choices=[str(i) for i in range(1, len(subnets)+1)])
                    iface, ip, network = subnets[int(choice_iface) - 1]
                else:
                    iface, ip, network = subnets[0]
                    console.print(f"Subred detectada automáticamente: {iface} - {network}")

                # Preguntar rango a escanear
                scan_range = choose_scan_range(ip, network)
                if scan_range:
                    devices = arp_scanner.scan_local_network(scan_range)
                    arp_scanner.print_devices(devices)
                else:
                    console.print("[yellow]Escaneo cancelado.[/yellow]")
                input("\nPresiona Enter para continuar...")

        elif choice == "3":
            console.print("Saliendo...")
            break

def main():
    show_main_menu(degraded_mode=False)

if __name__ == "__main__":
    main()
