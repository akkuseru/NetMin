from scapy.all import ARP, Ether, srp
from rich.table import Table
from rich.console import Console

console = Console()

def scan_local_network(target_range):
    """
    Escanea una red local usando ARP y devuelve una lista de dispositivos detectados.
    """
    if not target_range:
        return []

    arp_request = ARP(pdst=target_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    result = srp(packet, timeout=2, verbose=False)[0]

    devices = []
    for _, received in result:
        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc
        })

    return devices

def print_devices(devices):
    """
    Muestra en consola los dispositivos detectados en formato de tabla.
    """
    if not devices:
        console.print("[red]No se detectaron dispositivos.[/red]")
        return

    table = Table(title="Dispositivos detectados en la red")
    table.add_column("IP", style="cyan")
    table.add_column("MAC", style="magenta")

    for device in devices:
        table.add_row(device['ip'], device['mac'])

    console.print(table)
