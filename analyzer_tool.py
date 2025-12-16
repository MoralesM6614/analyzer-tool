#!/usr/bin/env python3
# ============================================
# ANALYZER TOOL
# Autor: Cracke2
# Contacto: https://t.me/Cracke2
# Plataforma: Android / Termux
# ============================================

import os
import sys
import socket
import requests
import ipaddress
import subprocess

# ================= VERSION =================
VERSION = "3.1"
GITHUB_REPO = "https://github.com/MoralesM6614/analyzer-tool"
VERSION_URL = "https://raw.githubusercontent.com/MoralesM6614/analyzer-tool/main/version.txt"

# ================= COLORES =================
C_RESET  = "\033[0m"
C_GREEN  = "\033[92m"
C_RED    = "\033[91m"
C_YELLOW = "\033[93m"
C_BLUE   = "\033[94m"
C_CYAN   = "\033[96m"
C_BOLD   = "\033[1m"

# ================= IDIOMA =================
LANG = "ES"

TEXT = {
    "ES": {
        "menu": "Seleccione una opción",
        "invalid": "Opción inválida",
        "press": "Presione ENTER para continuar...",
        "not_found": "No encontrados",
        "residential": "Red residencial",
        "vpn": "VPN / Proxy / Hosting",
        "updated": "✔ Actualizado",
        "update_available": "⚠ Update disponible",
        "no_connection": "Sin conexión",
    },
    "EN": {
        "menu": "Select an option",
        "invalid": "Invalid option",
        "press": "Press ENTER to continue...",
        "not_found": "Not found",
        "residential": "Residential network",
        "vpn": "VPN / Proxy / Hosting",
        "updated": "✔ Up to date",
        "update_available": "⚠ Update available",
        "no_connection": "No connection",
    }
}

# ================= UTILIDADES =================
def clear():
    os.system("clear")

def pause():
    input(f"\n{TEXT[LANG]['press']}")

def header(title):
    print(C_CYAN + "=" * 70)
    print(C_BOLD + title)
    print("=" * 70 + C_RESET)

# ================= UPDATE =================
def check_update():
    try:
        r = requests.get(VERSION_URL, timeout=5)
        remote = r.text.strip()
        if remote != VERSION:
            return ("update", remote)
        return ("ok", remote)
    except:
        return ("error", None)

def update_tool():
    clear()
    header("🔄 ACTUALIZAR HERRAMIENTA")

    print("Actualizando desde GitHub...\n")
    try:
        subprocess.run(["git", "pull"], check=True)
        print(C_GREEN + "\n✔ Herramienta actualizada correctamente" + C_RESET)
    except:
        print(C_RED + "\n✖ Error al actualizar (¿git instalado?)" + C_RESET)

    pause()

# ================= OPCIÓN 1 =================
def network_status():
    clear()
    header("🌐 ESTADO DE RED ACTUAL")

    try:
        ip_public = requests.get("https://api.ipify.org", timeout=5).text
        data = requests.get(
            "http://ip-api.com/json/?fields=country,countryCode,city,zip,isp,as,proxy,hosting",
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
    header("📌 ANÁLISIS TÉCNICO DE IP")

    ip = input("IP objetivo: ").strip()
    try:
        ipaddress.ip_address(ip)
    except:
        print(C_RED + "IP inválida" + C_RESET)
        pause()
        return

    data = requests.get(
        f"http://ip-api.com/json/{ip}?fields=country,countryCode,regionName,region,city,zip,lat,lon,timezone,isp,org,as,proxy,hosting",
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

ISP                : {data.get('isp')}
Organización       : {data.get('org')}
ASN                : {data.get('as')}
Tipo de IP         : {net_type}
""")
    pause()

# ================= OPCIÓN 3 =================
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

# ================= OPCIÓN 4 =================
def domain_ips():
    clear()
    header("🌐 IPv4 / IPv6")

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

    print("\nIPv4:")
    for i in ipv4: print(" ", i)
    print("\nIPv6:")
    for i in ipv6: print(" ", i)

    pause()

# ================= OPCIÓN 5 =================
def find_subdomains():
    clear()
    header("🧩 BUSCAR SUBDOMINIOS")

    domain = input("Dominio: ").strip()
    found = set()
    prefixes = ["www", "api", "m", "mail", "cdn", "static", "img"]

    for p in prefixes:
        try:
            socket.gethostbyname(f"{p}.{domain}")
            found.add(f"{p}.{domain}")
        except:
            pass

    if found:
        print(f"\nSubdominios encontrados ({len(found)}):")
        for s in sorted(found):
            print(" -", s)
    else:
        print(TEXT[LANG]["not_found"])
    pause()

# ================= OPCIÓN 6 =================
def site_info():
    clear()
    header("📄 INFORMACIÓN DEL SITIO")

    url = input("URL: ").strip()
    if not url.startswith("http"):
        url = "http://" + url

    try:
        r = requests.get(url, timeout=8)
        title = "N/A"
        if "<title>" in r.text.lower():
            title = r.text.lower().split("<title>")[1].split("</title>")[0]

        print(f"""
URL             : {r.url}
Título          : {title}
Servidor        : {r.headers.get('Server')}
Contenido       : {r.headers.get('Content-Type')}
Tamaño          : {len(r.content)/1024:.2f} KB
""")
    except:
        print("No responde")

    pause()

# ================= OPCIÓN 7 =================
def curl_tool():
    clear()
    header("🧰 CURL / HEADERS")
    url = input("URL: ").strip()
    os.system(f"curl -I {url}")
    pause()

# ================= MENÚ =================
def menu():
    status, remote = check_update()

    while True:
        clear()
        header("ANALYZER TOOL")

        if status == "ok":
            print(C_GREEN + f"Versión {VERSION} • {TEXT[LANG]['updated']}" + C_RESET)
        elif status == "update":
            print(C_YELLOW + f"Versión {VERSION} • {TEXT[LANG]['update_available']} ({remote})" + C_RESET)
        else:
            print(C_RED + TEXT[LANG]["no_connection"] + C_RESET)

        print("""
1) 🌐 Estado de red actual
2) 📌 Análisis técnico de IP
3) 📡 Resolver dominio DNS
4) 🌐 IPv4 / IPv6
5) 🧩 Buscar subdominios
6) 📄 Información del sitio
7) 🧰 Curl / Headers
8) 🔄 Actualizar herramienta
0) ❌ Salir
""")

        op = input(f"{TEXT[LANG]['menu']}: ").strip()

        if   op == "1": network_status()
        elif op == "2": analyze_ip()
        elif op == "3": resolve_dns()
        elif op == "4": domain_ips()
        elif op == "5": find_subdomains()
        elif op == "6": site_info()
        elif op == "7": curl_tool()
        elif op == "8": update_tool()
        elif op == "0": sys.exit()
        else:
            print(TEXT[LANG]["invalid"])
            pause()

if __name__ == "__main__":
    menu()