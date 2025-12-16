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
VERSION = "1.2"

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
        r = requests.get(
            "https://raw.githubusercontent.com/MoralesM6614/analyzer-tool/main/version.txt",
            timeout=5
        )
        remote = r.text.strip()
        if remote != VERSION:
            return ("update", remote)
        return ("ok", remote)
    except:
        return ("error", None)

def update_tool():
    clear()
    header("🔄 ACTUALIZAR HERRAMIENTA")
    try:
        subprocess.run(["git", "pull"], check=True)
        print(C_GREEN + "\n✔ Herramienta actualizada" + C_RESET)
    except:
        print(C_RED + "\n✖ Error al actualizar" + C_RESET)
    pause()

# ================= FAKE ADDRESS =================
def fake_address():
    clear()
    header("🏠 FAKE ADDRESS GENERATOR")

    country = input("Código de país (us, co, br, in, uk, de, auto): ").strip().lower()

    if country == "auto":
        try:
            geo = requests.get("http://ip-api.com/json/?fields=countryCode", timeout=5).json()
            country = geo.get("countryCode", "").lower()
        except:
            print("No se pudo detectar país")
            pause()
            return

    try:
        r = requests.get(f"https://randomuser.me/api/?nat={country}", timeout=10).json()
        u = r["results"][0]
        l = u["location"]

        print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Adress For {l['country']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Name : {u['name']['first']} {u['name']['last']}
- Street Address : {l['street']['number']} {l['street']['name']}
- City : {l['city']}
- State : {l['state']}
- Postal Code : {l['postcode']}
- Country : {l['country']}
- Phone : {u['phone']}
- Email : {u['email']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    except:
        print("País no soportado o error de conexión")

    pause()

# ================= FUNCIONES ORIGINALES =================
def network_status():
    clear()
    header("🌐 ESTADO DE RED ACTUAL")
    ip_public = requests.get("https://api.ipify.org").text
    data = requests.get("http://ip-api.com/json/").json()
    print(f"""
IP Pública : {ip_public}
País       : {data.get('country')}
Ciudad     : {data.get('city')}
ISP        : {data.get('isp')}
""")
    pause()

def analyze_ip():
    clear()
    header("📌 ANÁLISIS IP")
    ip = input("IP: ")
    try:
        ipaddress.ip_address(ip)
        data = requests.get(f"http://ip-api.com/json/{ip}").json()
        print(data)
    except:
        print("IP inválida")
    pause()

def resolve_dns():
    clear()
    header("📡 DNS")
    d = input("Dominio: ")
    try:
        print(socket.gethostbyname_ex(d)[2])
    except:
        print("No encontrado")
    pause()

def domain_ips():
    clear()
    header("🌐 IPv4 / IPv6")
    d = input("Dominio: ")
    try:
        for i in socket.getaddrinfo(d, None):
            print(i[4][0])
    except:
        print("No encontrado")
    pause()

def find_subdomains():
    clear()
    header("🧩 SUBDOMINIOS")
    d = input("Dominio: ")
    for p in ["www", "api", "mail", "cdn"]:
        try:
            socket.gethostbyname(f"{p}.{d}")
            print(f"{p}.{d}")
        except:
            pass
    pause()

def site_info():
    clear()
    header("📄 INFO WEB")
    url = input("URL: ")
    r = requests.get(url)
    print("Server:", r.headers.get("Server"))
    pause()

def curl_tool():
    clear()
    header("🧰 CURL")
    url = input("URL: ")
    os.system(f"curl -I {url}")
    pause()

# ================= MENÚ =================
def menu():
    status, remote = check_update()

    while True:
        clear()
        header("ANALYZER TOOL")

        if status == "ok":
            print(C_GREEN + f"Versión {VERSION} • Actualizado" + C_RESET)
        elif status == "update":
            print(C_YELLOW + f"Versión {VERSION} • Update disponible ({remote})" + C_RESET)
        else:
            print(C_RED + "Estado desconocido" + C_RESET)

        print("""
1) 🌐 Estado de red
2) 📌 Análisis IP
3) 📡 Resolver DNS
4) 🌐 IPv4 / IPv6
5) 🧩 Subdominios
6) 📄 Info sitio
7) 🧰 Curl
8) 🔄 Actualizar herramienta
9) 🏠 Fake Address Generator
0) ❌ Salir
""")

        op = input("Seleccione opción: ")

        if op == "1": network_status()
        elif op == "2": analyze_ip()
        elif op == "3": resolve_dns()
        elif op == "4": domain_ips()
        elif op == "5": find_subdomains()
        elif op == "6": site_info()
        elif op == "7": curl_tool()
        elif op == "8": update_tool()
        elif op == "9": fake_address()
        elif op == "0": sys.exit()
        else:
            print("Opción inválida")
            pause()

if __name__ == "__main__":
    menu()