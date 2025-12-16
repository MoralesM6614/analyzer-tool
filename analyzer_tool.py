#!/usr/bin/env python3
# ============================================
# ANALYZER TOOL
# Autor: Cracke2
# Contacto: https://t.me/Cracke2
# Plataforma: Android / Termux
# ============================================

import os, sys, socket, requests, ipaddress, subprocess, random, json, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# ================= INSTALACIÓN AUTOMÁTICA =================
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])

try:
    from faker import Faker
    import pycountry
except ImportError:
    print("🔄 Instalando dependencias...")
    install_package("Faker")
    install_package("pycountry")
    from faker import Faker
    import pycountry
    print("✅ Listo!")

# ================= VERSION =================
VERSION = "3.0"

# ================= COLORES =================
C_RESET  = "\u001B[0m"
C_GREEN  = "\u001B[92m"
C_RED    = "\u001B[91m"
C_YELLOW = "\u001B[93m"
C_BLUE   = "\u001B[94m"
C_CYAN   = "\u001B[96m"
C_BOLD   = "\u001B[1m"

# ================= IDIOMA =================
LANG = "ES"

TEXT = {
    "ES": {
        "menu": "Seleccione una opción",
        "press": "Presione ENTER para continuar...",
        "invalid": "Opción inválida",
        "again": "¿Generar nuevos datos? (S/N): ",
        "country_not_found": "País no encontrado. Usando formato genérico."
    },
    "EN": {
        "menu": "Select an option",
        "press": "Press ENTER to continue...",
        "invalid": "Invalid option",
        "again": "Generate new data? (Y/N): ",
        "country_not_found": "Country not found. Using generic format."
    }
}

# ================= FUNCIONES DE URL =================
def clean_url(url):
    """Limpia la URL acortada y devuelve la URL final."""
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        final_url = response.url
        if final_url == url:
            return "El enlace no está acortado."
        else:
            return f"URL final: {final_url}"
    except Exception as e:
        return f"Error al procesar el enlace: {e}"

def shorten_url():
    """Permite al usuario acortar un enlace mediante una API."""
    url = input("Introduce la URL que deseas acortar: ").strip()
    if not url.startswith("http"):
        url = "http://" + url

    response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
    if response.status_code == 200:
        print(f"Enlace acortado: {response.text}")
    else:
        print("Error al acortar el enlace.")

# ================= FUNCIONES DE IP Y SCAM =================
def check_ip_scam(ip):
    """Verifica si la IP está en la base de datos de ScamAnalytics."""
    api_key = 'TU_API_KEY_AQUI'
    url = f"https://api.scamanalytics.com/v1/ip/{ip}?apikey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['is_scam']:
            print(f"IP {ip} está marcada como potencialmente peligrosa.")
        else:
            print(f"IP {ip} es segura.")
    except Exception as e:
        print(f"Error al consultar la IP: {e}")

# ================= FAKE DATA GENERATOR =================
DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]

COUNTRIES = {
    "us": {"name": "United States", "cities": ["New York","Chicago","Philadelphia"], "states": ["NY","PA","CA"], "zip": lambda: str(random.randint(10000,99999))},
    "co": {"name": "Colombia", "cities": ["Bogotá","Medellín","Cali"], "states": ["Cundinamarca","Antioquia"], "zip": lambda: str(random.randint(110000,999999))},
    "br": {"name": "Brazil", "cities": ["São Paulo","Rio de Janeiro"], "states": ["SP","RJ"], "zip": lambda: f"{random.randint(10000,99999)}-{random.randint(100,999)}"},
    "ar": {"name": "Argentina", "cities": ["Buenos Aires","Córdoba"], "states": ["BA","CBA"], "zip": lambda: str(random.randint(1000,9999))},
    "cl": {"name": "Chile", "cities": ["Santiago","Valparaíso"], "states": ["RM","V"], "zip": lambda: str(random.randint(1000000,9999999))},
    "in": {"name": "India", "cities": ["Delhi","Mumbai","Bangalore"], "states": ["Delhi","MH","KA"], "zip": lambda: str(random.randint(100000,999999))},
    "uk": {"name": "United Kingdom", "cities": ["London","Manchester"], "states": ["England"], "zip": lambda: "SW1A " + str(random.randint(1,9)) + "AA"},
    "de": {"name": "Germany", "cities": ["Berlin","Munich"], "states": ["BE","BY"], "zip": lambda: str(random.randint(10000,99999))}
}

NAMES = ["Lucas","Mateo","Juan","Carlos","Ana","Maria","Sofia","Laura","Daniel","Pedro"]
LASTNAMES = ["Walker","Gomez","Perez","Silva","Rodriguez","Lopez","Fernandez","Muller","Schmidt"]

def generate_fake_data(code):
    c = COUNTRIES[code]
    name = f"{random.choice(NAMES)} {random.choice(LASTNAMES)}"
    email = f"{name.replace(' ','').lower()}{random.randint(10,999)}@{random.choice(DOMAINS)}"
    return {
        "name": name,
        "street": f"{random.randint(1,9999)} {random.choice(['Main','Market','Oak','Pine'])} Street",
        "city": random.choice(c["cities"]),
        "state": random.choice(c["states"]),
        "postal_code": c["zip"](),
        "country": c["name"],
        "email": email
    }

# ================= MENÚ =================
def menu():
    while True:
        clear()
        header("ANALYZER TOOL")
        print("""
1) 🌐 Estado de red actual
2) 📌 Análisis técnico de IP
3) 📡 Resolver dominio DNS
4) 🌐 IPv4 / IPv6
5) 🧩 Buscar subdominios
6) 📄 Información del sitio
7) 🧰 Curl / Headers
8) 🏠 Fake Address Generator
9) 🧳 Limpiar URL
10) 🔗 Acortar URL
11) 🔍 Verificar IP con ScamAnalytics
0) ❌ Salir
""")

        op = input(f"{TEXT[LANG]['menu']}: ").strip()

        if op == "1": network_status()
        elif op == "2": analyze_ip()
        elif op == "3": resolve_dns()
        elif op == "4": domain_ips()
        elif op == "5": find_subdomains()
        elif op == "6": site_info()
        elif op == "7": curl_tool()
        elif op == "8": fake_generator()
        elif op == "9": clean_url()
        elif op == "10": shorten_url()
        elif op == "11": check_ip_scam(input("Ingrese IP a verificar: "))
        elif op == "0": sys.exit()
        else:
            print(TEXT[LANG]["invalid"])
            pause()

if __name__ == "__main__":
    menu()