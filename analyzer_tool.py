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
VERSION = "1.0"

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
    print("Actualizando desde GitHub...\n")
    try:
        subprocess.run(["git", "pull"], check=True)
        print(C_GREEN + "\n✔ Herramienta actualizada correctamente" + C_RESET)
    except:
        print(C_RED + "\n✖ Error al actualizar (¿git instalado?)" + C_RESET)
    pause()

# ================= FAKE ADDRESS AUTO =================
def fake_address_auto():
    clear()
    header("🏠 FAKE ADDRESS GENERATOR (AUTO COUNTRY)")

    try:
        geo = requests.get(
            "http://ip-api.com/json/?fields=country,countryCode",
            timeout=5
        ).json()

        country = geo.get("country")
        code = geo.get("countryCode", "").lower()

        flags = {
            "us": "🇺🇸", "br": "🇧🇷", "co": "🇨🇴", "mx": "🇲🇽",
            "ar": "🇦🇷", "cl": "🇨🇱", "gb": "🇬🇧",
            "de": "🇩🇪", "in": "🇮🇳"
        }

        r = requests.get(
            f"https://randomuser.me/api/?nat={code}",
            timeout=10
        ).json()

        user = r["results"][0]
        loc = user["location"]

        print(f"""
Adress For {loc['country']} {flags.get(code, "")}
━━━━━━━━━━━━━━━━━━━
- Name : {user['name']['first']} {user['name']['last']}
- Street Address : {loc['street']['number']} {loc['street']['name']}
- City : {loc['city']}
- State : {loc['state']}
- Postal Code : {loc['postcode']}
- Country : {loc['country']}
- Phone : {user['phone']}
- Email : {user['email']}
━━━━━━━━━━━━━━━━━━━
""")

    except:
        print(C_RED + "No se pudo generar la dirección automáticamente" + C_RESET)

    pause()

# ================= OPCIONES EXISTENTES =================
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

def resolve_dns():
    clear()
    header("📡 RESOLVER DOMINIO (DNS)")
    domain = input("Dominio: ").strip()
    try:
        _, _, ips = socket.gethostbyname_ex(domain)
        for ip in ips:
            print("-", ip)
    except:
        print(TEXT[LANG]["not_found"])
    pause()

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
4) 🧰 Curl / Headers
5) 🏠 Fake Address (auto país)
6) 🔄 Actualizar herramienta
0) ❌ Salir
""")

        op = input(f"{TEXT[LANG]['menu']}: ").strip()

        if op == "1": network_status()
        elif op == "2": analyze_ip()
        elif op == "3": resolve_dns()
        elif op == "4": curl_tool()
        elif op == "5": fake_address_auto()
        elif op == "6": update_tool()
        elif op == "0": sys.exit()
        else:
            print(TEXT[LANG]["invalid"])
            pause()

if __name__ == "__main__":
    menu()