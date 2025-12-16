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
import random

# ============ AUTO-INSTALADOR DEPENDENCIAS ============
def ensure_dependency(module, pip_name=None):
    try:
        __import__(module)
    except ImportError:
        print(f"[+] Instalando dependencia faltante: {module}")
        pkg = pip_name if pip_name else module
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", pkg
        ])

ensure_dependency("faker")
ensure_dependency("pycountry")
ensure_dependency("phonenumbers")

from faker import Faker
import pycountry
import unicodedata
import phonenumbers
from phonenumbers import PhoneNumberFormat

# ================= VERSION =================
VERSION = "1.2"
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
    try:
        subprocess.run(["git", "pull"], check=True)
        print(C_GREEN + "✔ Herramienta actualizada" + C_RESET)
    except:
        print(C_RED + "✖ Error al actualizar" + C_RESET)
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
        print(C_RED + "Error obteniendo datos" + C_RESET)
        pause()
        return

    net_type = TEXT[LANG]["vpn"] if data.get("proxy") or data.get("hosting") else TEXT[LANG]["residential"]

    print(f"""
IP pública    : {ip_public}
País          : {data.get('country')} [{data.get('countryCode')}]
Ciudad        : {data.get('city')}
ZIP           : {data.get('zip')}
ISP           : {data.get('isp')}
ASN           : {data.get('as')}
Tipo de red   : {net_type}
""")
    pause()

# ================= OPCIÓN 2 =================
def analyze_ip():
    clear()
    header("📌 ANÁLISIS DE IP")
    ip = input("IP objetivo: ").strip()
    try:
        ipaddress.ip_address(ip)
    except:
        print(C_RED + "IP inválida" + C_RESET)
        pause()
        return

    data = requests.get(
        f"http://ip-api.com/json/{ip}?fields=country,countryCode,regionName,city,zip,isp,as,proxy,hosting",
        timeout=8
    ).json()

    net_type = TEXT[LANG]["vpn"] if data.get("proxy") or data.get("hosting") else TEXT[LANG]["residential"]

    print(f"""
IP      : {ip}
País    : {data.get('country')} [{data.get('countryCode')}]
Ciudad  : {data.get('city')}
ZIP     : {data.get('zip')}
ISP     : {data.get('isp')}
ASN     : {data.get('as')}
Tipo    : {net_type}
""")
    pause()

# ================= OPCIÓN 3 =================
def resolve_dns():
    clear()
    header("📡 RESOLVER DNS")
    domain = input("Dominio: ").strip()
    try:
        _, _, ips = socket.gethostbyname_ex(domain)
        for ip in ips:
            print("-", ip)
    except:
        print(TEXT[LANG]["not_found"])
    pause()

# ================= OPCIÓN 4 =================
def domain_ips():
    clear()
    header("🌐 IPv4 / IPv6")
    domain = input("Dominio: ").strip()
    try:
        for info in socket.getaddrinfo(domain, None):
            print(info[4][0])
    except:
        print(TEXT[LANG]["not_found"])
    pause()

# ================= OPCIÓN 5 =================
def find_subdomains():
    clear()
    header("🧩 SUBDOMINIOS")
    domain = input("Dominio: ").strip()
    prefixes = ["www", "api", "mail", "cdn"]
    encontrados = False
    for p in prefixes:
        try:
            socket.gethostbyname(f"{p}.{domain}")
            print("-", f"{p}.{domain}")
            encontrados = True
        except:
            pass
    if not encontrados:
        print(TEXT[LANG]["not_found"])
    pause()

# ================= OPCIÓN 6 =================
def site_info():
    clear()
    header("📄 INFO DEL SITIO")
    url = input("URL: ").strip()
    if not url.startswith("http"):
        url = "http://" + url
    try:
        r = requests.get(url, timeout=8)
        print("Servidor:", r.headers.get("Server"))
        print("Tipo:", r.headers.get("Content-Type"))
    except:
        print("No responde")
    pause()

# ================= OPCIÓN 7 =================
def curl_tool():
    clear()
    header("🧰 CURL")
    url = input("URL: ").strip()
    os.system(f"curl -I {url}")
    pause()

# ====== FAKE ADDRESS FUNCTIONS ======
def normalizar(txt):
    txt = txt.lower()
    txt = unicodedata.normalize("NFKD", txt)
    return "".join(c for c in txt if not unicodedata.combining(c))

def resolver_pais(nombre):
    nombre = normalizar(nombre)
    for c in pycountry.countries:
        if normalizar(c.name) == nombre:
            return c.alpha_2
        if hasattr(c, "official_name") and normalizar(c.official_name) == nombre:
            return c.alpha_2
    return None

def obtener_locale(alpha2):
    for loc in Faker().locales:
        if loc.endswith("_" + alpha2):
            return loc
    return None

def telefono_real(alpha2):
    try:
        num = phonenumbers.example_number(alpha2)
        return phonenumbers.format_number(num, PhoneNumberFormat.INTERNATIONAL)
    except:
        return "N/A"

# ================= OPCIÓN 8 =================
def generate_identity():
    clear()
    header("🏠 FAKE ADDRESS GENERATOR")

    pais = input("País a generar (nombre completo): ").strip()
    alpha2 = resolver_pais(pais)

    if not alpha2:
        print(C_RED + "País no reconocido" + C_RESET)
        pause()
        return

    locale = obtener_locale(alpha2)
    if not locale:
        print(C_RED + "País sin soporte de direcciones" + C_RESET)
        pause()
        return

    fake = Faker(locale)
    Faker.seed(None)

    nombre_completo = fake.name()
    partes = nombre_completo.split(" ", 1)
    nombre = partes[0]
    apellido = partes[1] if len(partes) > 1 else ""

    email = f"{nombre}.{apellido}".lower().replace(" ", "") + "@gmail.com"

    print(C_GREEN + "IDENTIDAD GENERADA" + C_RESET)
    print(f"""
Nombre      : {nombre} {apellido}
Dirección   : {fake.street_address()}
Ciudad      : {fake.city()}
Estado      : {fake.state() if hasattr(fake, 'state') else 'N/A'}
ZIP         : {fake.postcode() if hasattr(fake, 'postcode') else 'N/A'}
País        : {pais.title()}
Teléfono    : {telefono_real(alpha2)}
Email       : {email}
""")
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
8) 🏠 Fake Address Generator
9) 🔄 Actualizar herramienta
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
        elif op == "8": generate_identity()
        elif op == "9": update_tool()
        elif op == "0": sys.exit()
        else:
            print(TEXT[LANG]["invalid"])
            pause()

if __name__ == "__main__":
    menu()