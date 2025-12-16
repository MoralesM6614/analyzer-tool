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

# ================= VERSION =================
VERSION = "3.2"

# ================= COLORES =================
C_RESET  = "\033[0m"
C_GREEN  = "\033[92m"
C_RED    = "\033[91m"
C_YELLOW = "\033[93m"
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
        "updated": "✔ Actualizado"
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

# ================= EMAIL REAL =================
def generate_email(first, last, cc):
    domains = {
        "us": ["gmail.com", "yahoo.com", "outlook.com"],
        "co": ["gmail.com", "outlook.com"],
        "mx": ["gmail.com", "hotmail.com"],
        "ar": ["gmail.com"],
        "cl": ["gmail.com"],
        "br": ["gmail.com", "hotmail.com"],
        "in": ["gmail.com", "yahoo.in"],
        "de": ["gmail.com", "web.de"],
        "uk": ["gmail.com", "outlook.co.uk"]
    }
    return f"{first.lower()}.{last.lower()}@{random.choice(domains[cc])}"

# ================= CPF / CEP BR =================
def generate_cpf():
    nums = [random.randint(0,9) for _ in range(9)]
    for _ in range(2):
        val = sum((len(nums)+1-i)*v for i,v in enumerate(nums)) % 11
        nums.append(0 if val < 2 else 11-val)
    return "".join(map(str, nums))

def generate_cep():
    return f"{random.randint(10000,99999)}-{random.randint(100,999)}"

# ================= FAKE ADDRESS =================
def fake_address():
    clear()
    header("🏠 FAKE ADDRESS GENERATOR")

    country = input("País (us co br mx ar cl in uk de): ").strip().lower()

    data = {
        "us": ("United States", "New York", "California"),
        "co": ("Colombia", "Medellín", "Antioquia"),
        "br": ("Brazil", "São Paulo", "SP"),
        "mx": ("Mexico", "Guadalajara", "Jalisco"),
        "ar": ("Argentina", "Buenos Aires", "BA"),
        "cl": ("Chile", "Santiago", "RM"),
        "in": ("India", "Mumbai", "Maharashtra"),
        "uk": ("United Kingdom", "London", "England"),
        "de": ("Germany", "Berlin", "Berlin"),
    }

    if country not in data:
        print(C_RED + "País no soportado" + C_RESET)
        pause()
        return

    first = random.choice(["Lucas","Daniel","Mateo","Raj","Arjun","John","Pedro","Luis","Carlos"])
    last  = random.choice(["Walker","Gómez","Silva","Patel","Müller","Smith","Fernández"])

    email = generate_email(first, last, country)
    street = f"{random.randint(10,9999)} {random.choice(['Market St','Main St','Oak Ave','Park Rd'])}"

    print(f"""
Adress For {data[country][0]}
━━━━━━━━━━━━━━━━━━━━
Name        : {first} {last}
Street      : {street}
City        : {data[country][1]}
State       : {data[country][2]}
Postal Code : {generate_cep() if country=='br' else random.randint(10000,99999)}
Country     : {data[country][0]}
Email       : {email}
""")

    if country == "br":
        print(f"CPF         : {generate_cpf()}")

    pause()

# ================= ANALYZER FUNCTIONS =================
def network_status():
    clear()
    header("🌐 ESTADO DE RED")
    ip = requests.get("https://api.ipify.org").text
    data = requests.get("http://ip-api.com/json").json()
    print(f"IP: {ip}\nPaís: {data.get('country')}\nISP: {data.get('isp')}")
    pause()

def analyze_ip():
    clear()
    header("📌 ANÁLISIS IP")
    ip = input("IP: ")
    try:
        ipaddress.ip_address(ip)
        data = requests.get(f"http://ip-api.com/json/{ip}").json()
        for k,v in data.items():
            print(f"{k:15}: {v}")
    except:
        print("IP inválida")
    pause()

def resolve_dns():
    clear()
    header("📡 DNS")
    d = input("Dominio: ")
    try:
        for i in socket.gethostbyname_ex(d)[2]:
            print(i)
    except:
        print("No encontrado")
    pause()

def domain_ips():
    clear()
    header("🌐 IPv4 / IPv6")
    d = input("Dominio: ")
    try:
        for i in socket.getaddrinfo(d,None):
            print(i[4][0])
    except:
        print("No encontrado")
    pause()

def find_subdomains():
    clear()
    header("🧩 SUBDOMINIOS")
    d = input("Dominio: ")
    for p in ["www","api","mail","cdn"]:
        try:
            socket.gethostbyname(f"{p}.{d}")
            print(f"{p}.{d}")
        except:
            pass
    pause()

def site_info():
    clear()
    header("📄 INFO WEB")
    u = input("URL: ")
    if not u.startswith("http"):
        u = "http://" + u
    r = requests.get(u)
    print("Servidor:", r.headers.get("Server"))
    print("Tipo:", r.headers.get("Content-Type"))
    pause()

def curl_tool():
    clear()
    header("🧰 CURL")
    os.system(f"curl -I {input('URL: ')}")
    pause()

# ================= MENÚ =================
def menu():
    while True:
        clear()
        header("ANALYZER TOOL")
        print(C_GREEN + f"Versión {VERSION} • {TEXT[LANG]['updated']}" + C_RESET)

        print("""
1) 🌐 Estado de red
2) 📌 Análisis IP
3) 📡 Resolver DNS
4) 🌐 IPv4 / IPv6
5) 🧩 Buscar subdominios
6) 📄 Información del sitio
7) 🧰 Curl / Headers
8) 🏠 Fake Address Generator
0) ❌ Salir
""")

        op = input(f"{TEXT[LANG]['menu']}: ")

        if   op == "1": network_status()
        elif op == "2": analyze_ip()
        elif op == "3": resolve_dns()
        elif op == "4": domain_ips()
        elif op == "5": find_subdomains()
        elif op == "6": site_info()
        elif op == "7": curl_tool()
        elif op == "8": fake_address()
        elif op == "0": sys.exit()
        else:
            print(TEXT[LANG]["invalid"])
            pause()

if __name__ == "__main__":
    menu()