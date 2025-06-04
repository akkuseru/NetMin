# scanner/network_utils.py
import psutil
import ipaddress

def get_local_subnets_with_interfaces(min_prefix=24):
    """
    Devuelve una lista de tuplas (iface, ip_local, subred_cidr)
    con las subredes IPv4 activas (excluye loopback).
    Filtra subredes que tengan prefijo menor o igual a min_prefix (ej: /24).
    """
    subnets = []
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family.name == 'AF_INET' and not addr.address.startswith("127."):
                ip = addr.address
                netmask = addr.netmask
                try:
                    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                    # Aceptamos subredes con prefijo >= min_prefix (más específicas o iguales)
                    if network.prefixlen >= min_prefix:
                        subnets.append((iface, ip, str(network)))
                except ValueError:
                    continue
    return subnets

def detect_vpn_connections():
    """Detecta posibles conexiones VPN en base al nombre de las interfaces."""
    vpn_keywords = ["tun", "tap", "vpn", "ppp", "wg"]
    active_vpns = []
    for iface in psutil.net_if_addrs().keys():
        if any(keyword in iface.lower() for keyword in vpn_keywords):
            active_vpns.append(iface)
    return active_vpns

def get_active_interfaces():
    """Devuelve un diccionario de interfaces activas con sus IPs."""
    interfaces = {}
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family.name == 'AF_INET' and not addr.address.startswith("127."):
                interfaces[iface] = addr.address
    return interfaces

def is_interface_virtual(iface_name):
    """Intenta determinar si una interfaz es virtual."""
    virtual_keywords = ["docker", "br-", "virbr", "vmnet", "vbox", "lo", "tun", "tap"]
    return any(keyword in iface_name.lower() for keyword in virtual_keywords)
