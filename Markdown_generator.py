import re
import os
from collections import defaultdict

#Fichiers
INPUT_FILE = "DumpFile.txt"
OUTPUT_MD = "analyse_tcpdump.md"

#sépare les champs
line_pattern = re.compile(
    r'^(?P<time>\d{2}:\d{2}:\d{2}\.\d+)\s+'
    r'(?P<proto>IP|IP6)\s+'
    r'(?P<src>\S+)\s+>\s+'
    r'(?P<dst>\S+):\s*(?P<rest>.*)'
)

#analyse le reste de l'entete
def extract_optional(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else ""

#separe les colonnes dans le markdown
def split_ip_port(value):
    parts = value.rsplit(".", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return value, ""

#Comptes les IP sources
ip_source_count = defaultdict(int)

#tri les différentes tramse dans une liste de dictionnaire
frames = []

#Lecture du fichier tcpdump
with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:

        # Ignore hexadécimal
        if line.startswith("\t") or line.startswith(" "):
            continue

        #ignore les lignes non conforme
        match = line_pattern.match(line)
        if not match:
            continue

        #extraction des champs reste
        rest = match.group("rest")

        #separation IP/port
        src_ip, src_port = split_ip_port(match.group("src"))
        dst_ip, dst_port = split_ip_port(match.group("dst"))

        #Comptage IP source
        ip_source_count[src_ip] += 1

        #ajoute les différents champs dans la ligne
        frames.append({
            "time": match.group("time"),
            "proto": match.group("proto"),
            "src_ip": src_ip,
            "src_port": src_port,
            "dst_ip": dst_ip,
            "dst_port": dst_port,
            "flags": extract_optional(r'Flags\s+\[([^\]]+)\]', rest),
            "seq": extract_optional(r'seq\s+([^,]+)', rest),
            "ack": extract_optional(r'ack\s+(\d+)', rest),
            "length": extract_optional(r'length\s+(\d+)', rest),
        })


#Creation Markdown
with open(OUTPUT_MD, "w", encoding="utf-8") as md:
    md.write("# Analyse tcpdump\n\n")

    md.write("## Résumé\n\n")
    md.write(f"- Nombre total de trames : **{len(frames)}**\n")
    md.write(f"- Nombre d'IP sources uniques : **{len(ip_source_count)}**\n\n")


    md.write("## Top IP sources\n\n")
    md.write("| IP source | Nombre de trames |\n")
    md.write("|-----------|------------------|\n")

    #ecrit les différentes IP et leurs nombres
    for ip, count in sorted(ip_source_count.items(), key=lambda x: x[1], reverse=True):
        md.write(f"| {ip} | {count} |\n")

    md.write("\n")
    md.write("## Détails des trames\n\n")
    md.write("| Heure | Proto | IP source | Port src | IP dest | Port dest | Flags | Seq | Ack | Taille |\n")
    md.write("|-------|-------|-----------|----------|----------|-----------|-------|-----|-----|--------|\n")

    #Ecrit tout les champs
    for f in frames:
        md.write(
            f"| {f['time']} | {f['proto']} | {f['src_ip']} | {f['src_port']} | "
            f"{f['dst_ip']} | {f['dst_port']} | {f['flags']} | "
            f"{f['seq']} | {f['ack']} | {f['length']} |\n"
        )
