#!/usr/bin/env python3
# ============================================
# ANALYZER TOOL
# Contacto: https://t.me/Cracke2
# ============================================

import os
import sys
import socket
import requests
import ipaddress
from urllib.parse import urlparse

# ================= VERSION =================
VERSION = "3.0"

# ================= COLORES =================
C_RESET = "\033[0m"
C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_CYAN = "\033[96m"
C_WHITE = "\033[97m"
C_BOLD = "\033[1m"

# ================= IDIOMA =================
LANG = "ES"

TEXT = {
    "ES": {
        "menu": "Seleccione una opción",
        "invalid": "Opción inválida",
        "press": "Presione ENTER para continuar...",
        "not_found": "No encontrados",
        "exit": "Salir",
        "domain": "Dominio",
        "ip": "IP",
        "yes": "Sí",
        "no": "No",
        "residential": "Red residencial",
        "vpn": "VPN / Proxy / Hosting"
    },
    "EN": {
        "menu": "Select an option",
        "invalid": "Invalid option",
        "press": "Press ENTER to continue...",
        "not_found": "Not found",
        "exit": "Exit",
        "domain": "Domain",
        "ip": "IP",
        "yes": "Yes",
        "no": "No",
        "residential": "Residential network",
        "vpn": "VPN / Proxy / Hosting"
    }
}

# ================= UPDATE ONLINE =================
def check_update():
    try:
        url = "https://raw.githubusercontent.com/MoralesM6614/analyzer-tool/main/version.txt"
        remote_version = requests.get(url, timeout=5).text.strip()

        if remote_version != VERSION:
            return ("update", remote_version)
        else:
            return ("ok", VERSION)
    except:
        return ("error", None)

# ================= UTILIDADES =================
def clear():
    os.system("clear")

def pause():
    input(f"\n{TEXT[LANG]['press']}")

def header(title):
    print(C_CYAN + "=" * 70)
    print(C_BOLD + title)
    print("=" * 70 + C_RESET)

# ================= OPCIÓN 1 =================
def network_status():
    clear()
    header("🌐 ESTADO DE RED ACTUAL")

    try:
        ip_public = requests.get("https://api.ipify.org", timeout=5).text
        data = requests.get(
            "http://ip-api.com/json/?fields=status,country,countryCode,city,zip,isp,as,proxy,hosting",
            timeout=8
        ).json()
    except:
        print(C_RED + "Error obteniendo datos de red" + C_RESET)
        pause()
        return

    net_type = TEXT[LANG]["vpn"] if data.get("proxy") or data.get("hosting") else TEXT[LANG]["residential"]

    print(f"""
IP pública      : {ip_public}
País            : {data.get('country')} [{data.get('countryCode')}]
Ciudad          : {data.get('city')}
ZIP             : {data.get('zip')}
Proveedor red   : {data.get('isp')}
ASN             : {data.get('as')}
Tipo de red     : {net_type}
""")
    pause()

# ================= OPCIÓN 2 =================
def analyze_ip():
    clear()
    header("📌 ANÁLISIS TÉCNICO DE DIRECCIÓN IP")

    ip = input("IP objetivo: ").strip()
    try:
        ipaddress.ip_address(ip)
    except:
        print(C_RED + "IP inválida" + C_RESET)
        pause()
        return

    data = requests.get(
        f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,region,city,zip,lat,lon,timezone,isp,org,as,proxy,hosting",
        timeout=8
    ).json()

    net_type = TEXT[LANG]["vpn"] if data.get("proxy") or data.get("hosting") else TEXT[LANG]["residential"]

    print(f"""
IP objetivo        : {ip}
País               : {data.get('country')} [{data.get('countryCode')}]
Región             : {data.get('regionName')} ({data.get('region')})
Ciudad             : {data.get('city')}
Código postal      : {data.get('zip')}
Zona horaria       : {data.get('timezone')}
Coordenadas        : {data.get('lat')}, {data.get('lon')}

Proveedor (ISP)    : {data.get('isp')}
Organización       : {data.get('org')}
ASN                : {data.get('as')}

Tipo de IP         : {net_type}
""")
    pause()

# ================= OPCIÓN 3 =================
def geolocation_only():
    clear()
    header("🗺️ GEOLOCALIZACIÓN DE IP")

    ip = input("IP: ").strip()
    data = requests.get(f"http://ip-api.com/json/{ip}", timeout=8).json()

    print(f"""
País        : {data.get('country')}
Región      : {data.get('regionName')}
Ciudad      : {data.get('city')}
ZIP         : {data.get('zip')}
Zona horaria: {data.get('timezone')}
""")
    pause()

# ================= OPCIÓN 4 =================
def resolve_dns():
    clear()
    header("📡 RESOLVER DOMINIO (DNS)")

    domain = input("Dominio: ").strip()
    try:
        _, _, ips = socket.gethostbyname_ex(domain)
        for ip in ips:
            print(f"- {ip}")
    except:
        print(TEXT[LANG]["not_found"])
    pause()

# ================= OPCIÓN 5 =================
def domain_ips():
    clear()
    header("🌐 DIRECCIONES IPv4 / IPv6")

    domain = input("Dominio: ").strip()
    ipv4, ipv6 = set(), set()

    try:
        for info in socket.getaddrinfo(domain, None):
            if info[0] == socket.AF_INET:
                ipv4.add(info[4][0])
            elif info[0] == socket.AF_INET6:
                ipv6.add(info[4][0])
    except:
        print(TEXT[LANG]["not_found"])
        pause()
        return

    print("IPv4:")
    for ip in ipv4:
        print(f"  {ip}")
    print("\nIPv6:")
    for ip in ipv6:
        print(f"  {ip}")
    pause()

# ================= OPCIÓN 6 =================
def find_subdomains():
    clear()
    header("🧩 BUSCAR SUBDOMINIOS")

    domain = input("Dominio: ").strip()
    found = set()

    prefixes = ["www", "api", "m", "mail", "cdn", "static", "img"]
    for p in prefixes:
        host = f"{p}.{domain}"
        try:
            socket.gethostbyname(host)
            found.add(host)
        except:
            pass

    if found:
        print(f"\nSubdominios encontrados ({len(found)}):")
        for s in sorted(found):
            print(f" - {s}")
    else:
        print(TEXT[LANG]["not_found"])
    pause()

# ================= OPCIÓN 7 =================
def site_status():
    clear()
    header("🔍 ESTADO DEL SITIO WEB")

    url = input("URL: ").strip()
    if not url.startswith("http"):
        url = "http://" + url

    try:
        r = requests.get(url, timeout=8, allow_redirects=True)
        print(f"""
URL final : {r.url}
HTTP      : {r.status_code}
Servidor  : {r.headers.get('Server')}
""")
    except:
        print("No responde")
    pause()

# ================= OPCIÓN 8 =================
def site_info():
    clear()
    header("📄 INFORMACIÓN BÁSICA DEL SITIO")

    url = input("URL: ").strip()
    if not url.startswith("http"):
        url = "http://" + url

    r = requests.get(url, timeout=8)
    html = r.text.lower()

    title = html.split("<title>")[1].split("</title>")[0] if "<title>" in html else "N/A"

    print(f"""
Título        : {title}
Servidor      : {r.headers.get('Server')}
Contenido     : {r.headers.get('Content-Type')}
Tamaño        : {len(r.content) / 1024:.2f} KB
""")
    pause()

# ================= OPCIÓN 9 =================
def domain_network_info():
    clear()
    header("🌍 INFORMACIÓN DE RED DEL DOMINIO")

    domain = input("Dominio: ").strip()
    ip = socket.gethostbyname(domain)
    data = requests.get(f"http://ip-api.com/json/{ip}", timeout=8).json()

    print(f"""
IP infraestructura : {ip}
Proveedor          : {data.get('isp')}
ASN                : {data.get('as')}
País               : {data.get('country')}
""")
    pause()

# ================= OPCIÓN 10 =================
def curl_tool():
    clear()
    header("🧰 CURL / HEADERS")

    url = input("URL: ").strip()
    os.system(f"curl -I {url}")
    pause()

# ================= MENÚ =================
def menu():
    update_status, remote_version = check_update()

    while True:
        clear()
        header("ANALYZER TOOL")

        if update_status == "update":
            print(C_YELLOW + f"Versión {VERSION} • ⚠ Update disponible ({remote_version})" + C_RESET)
        elif update_status == "ok":
            print(C_GREEN + f"Versión {VERSION} • ✔ Actualizado" + C_RESET)
        else:
            print(C_RED + "Estado de versión desconocido (sin conexión)" + C_RESET)

        print("""
1) 🌐 Estado de red actual
2) 📌 Análisis técnico de IP
3) 🗺️ Geolocalización
4) 📡 Resolver dominio DNS
5) 🌐 Direcciones IPv4 / IPv6
6) 🧩 Buscar subdominios
7) 🔍 Estado del sitio web
8) 📄 Información básica del sitio
9) 🌍 Red del dominio
10) 🧰 Curl / Headers
0) ❌ Salir
""")

        op = input(f"{TEXT[LANG]['menu']}: ").strip()

        if op == "1": network_status()
        elif op == "2": analyze_ip()
        elif op == "3": geolocation_only()
        elif op == "4": resolve_dns()
        elif op == "5": domain_ips()
        elif op == "6": find_subdomains()
        elif op == "7": site_status()
        elif op == "8": site_info()
        elif op == "9": domain_network_info()
        elif op == "10": curl_tool()
        elif op == "0": sys.exit()
        else:
            print(TEXT[LANG]["invalid"])
            pause()

if __name__ == "__main__":
    menu()