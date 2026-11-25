"""
pc_info.py
==========
Script simples para exibir informações do computador (PC).
Útil para inventário de hardware, diagnósticos rápidos e aprendizado.

Requisitos:
- Python 3.8+
- psutil (opcional, para informações detalhadas de memória, disco e rede)
"""

import argparse
import json
import platform
import socket
import os
from datetime import datetime

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def get_system_info():
    """Retorna informações básicas do sistema operacional."""
    uname = platform.uname()
    return {
        "Sistema": uname.system,
        "Nome do nó (hostname)": uname.node,
        "Versão": uname.version,
        "Máquina": uname.machine,
        "Processador": uname.processor,
        "Usuário": os.getlogin() if hasattr(os, "getlogin") else os.environ.get("USERNAME", "desconhecido"),
        "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }


def get_cpu_info():
    """Retorna informações da CPU."""
    if not HAS_PSUTIL:
        return {"Aviso": "Instale o psutil para informações detalhadas da CPU."}

    return {
        "Núcleos físicos": psutil.cpu_count(logical=False),
        "Núcleos lógicos": psutil.cpu_count(logical=True),
        "Uso atual (%)": psutil.cpu_percent(interval=1),
        "Frequência atual (MHz)": round(psutil.cpu_freq().current, 2) if psutil.cpu_freq() else "N/A",
    }


def get_memory_info():
    """Retorna informações da memória RAM."""
    if not HAS_PSUTIL:
        return {"Aviso": "Instale o psutil para informações detalhadas da memória."}

    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "Memória total (GB)": round(mem.total / (1024 ** 3), 2),
        "Memória disponível (GB)": round(mem.available / (1024 ** 3), 2),
        "Memória em uso (%)": mem.percent,
        "Swap total (GB)": round(swap.total / (1024 ** 3), 2),
        "Swap em uso (%)": swap.percent,
    }


def get_disk_info():
    """Retorna informações dos discos."""
    if not HAS_PSUTIL:
        return {"Aviso": "Instale o psutil para informações detalhadas de disco."}

    discos = []
    for part in psutil.disk_partitions(all=False):
        try:
            uso = psutil.disk_usage(part.mountpoint)
            discos.append({
                "Dispositivo": part.device,
                "Ponto de montagem": part.mountpoint,
                "Sistema de arquivos": part.fstype,
                "Total (GB)": round(uso.total / (1024 ** 3), 2),
                "Usado (GB)": round(uso.used / (1024 ** 3), 2),
                "Livre (GB)": round(uso.free / (1024 ** 3), 2),
                "Uso (%)": uso.percent,
            })
        except PermissionError:
            continue
    return discos


def get_network_info():
    """Retorna informações de rede."""
    try:
        hostname = socket.gethostname()
        ip_local = socket.gethostbyname(hostname)
    except Exception:
        hostname = "N/A"
        ip_local = "N/A"

    info = {
        "Hostname": hostname,
        "IP local": ip_local,
    }

    if HAS_PSUTIL:
        interfaces = psutil.net_if_addrs()
        redes = []
        for iface, addrs in interfaces.items():
            for addr in addrs:
                if str(addr.family).startswith("AF_INET"):
                    redes.append({
                        "Interface": iface,
                        "IP": addr.address,
                        "Máscara": addr.netmask,
                    })
        info["Interfaces de rede"] = redes

    return info


def coletar_tudo():
    """Coleta todas as informações em um único dicionário."""
    return {
        "sistema": get_system_info(),
        "cpu": get_cpu_info(),
        "memoria": get_memory_info(),
        "discos": get_disk_info(),
        "rede": get_network_info(),
    }


def print_section(titulo):
    print("\n" + "=" * 50)
    print(f" {titulo}")
    print("=" * 50)


def print_dict(dados, indent=0):
    prefixo = "  " * indent
    for chave, valor in dados.items():
        if isinstance(valor, list):
            print(f"{prefixo}{chave}:")
            for item in valor:
                if isinstance(item, dict):
                    print_dict(item, indent + 1)
                else:
                    print(f"{prefixo}  - {item}")
        elif isinstance(valor, dict):
            print(f"{prefixo}{chave}:")
            print_dict(valor, indent + 1)
        else:
            print(f"{prefixo}{chave}: {valor}")


def salvar_txt(dados, nome_arquivo="pc_info.txt"):
    """Salva as informações em um arquivo de texto."""
    linhas = []
    linhas.append("🖥️  PC INFO - Informações do Computador")
    linhas.append(f"Gerado em: {dados['sistema']['Data/Hora']}")
    linhas.append("=" * 50)

    secoes = [
        ("Sistema", dados.get("sistema", {})),
        ("CPU", dados.get("cpu", {})),
        ("Memória RAM", dados.get("memoria", {})),
        ("Discos", dados.get("discos", [])),
        ("Rede", dados.get("rede", {})),
    ]

    for titulo, conteudo in secoes:
        linhas.append(f"\n{titulo}")
        linhas.append("-" * 30)
        if isinstance(conteudo, list):
            for item in conteudo:
                if isinstance(item, dict):
                    for k, v in item.items():
                        linhas.append(f"  {k}: {v}")
                    linhas.append("")
        elif isinstance(conteudo, dict):
            for k, v in conteudo.items():
                linhas.append(f"  {k}: {v}")

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    return nome_arquivo


def salvar_json(dados, nome_arquivo="pc_info.json"):
    """Salva as informações em um arquivo JSON."""
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    return nome_arquivo


def main():
    parser = argparse.ArgumentParser(
        description="Exibe informações do computador (PC)."
    )
    parser.add_argument(
        "--salvar-txt",
        metavar="ARQUIVO",
        help="Salva as informações em um arquivo de texto (ex: --salvar-txt relatorio.txt)",
    )
    parser.add_argument(
        "--salvar-json",
        metavar="ARQUIVO",
        help="Salva as informações em um arquivo JSON (ex: --salvar-json info.json)",
    )
    parser.add_argument(
        "--apenas-saida",
        action="store_true",
        help="Não exibe no terminal, apenas salva nos arquivos informados",
    )
    args = parser.parse_args()

    dados = coletar_tudo()

    if args.salvar_txt:
        caminho_txt = salvar_txt(dados, args.salvar_txt)
        if not args.apenas_saida:
            print(f"💾 Relatório salvo em: {caminho_txt}")

    if args.salvar_json:
        caminho_json = salvar_json(dados, args.salvar_json)
        if not args.apenas_saida:
            print(f"💾 JSON salvo em: {caminho_json}")

    if not args.apenas_saida and not args.salvar_txt and not args.salvar_json:
        # Modo interativo: exibe tudo no terminal
        print("\n🖥️  PC INFO - Informações do Computador")
        print_section("Sistema")
        print_dict(get_system_info())

        print_section("CPU")
        print_dict(get_cpu_info())

        print_section("Memória RAM")
        print_dict(get_memory_info())

        print_section("Discos")
        discos = get_disk_info()
        if isinstance(discos, list) and discos:
            for disco in discos:
                print_dict(disco)
                print("-" * 40)
        else:
            print_dict(discos)

        print_section("Rede")
        print_dict(get_network_info())

        print("\n✅ Concluído!\n")
    elif not args.apenas_saida:
        print("\n✅ Arquivos gerados com sucesso!\n")


if __name__ == "__main__":
    main()
