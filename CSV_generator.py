import re
import csv
import os
from collections import defaultdict

# Ouvrir les fichiers 
INPUT_FILE = "DumpFile.txt"
OUTPUT_CSV = "resultats.csv"
ANALYSE_CSV = "analyse_ip_sources.csv"

# Séparé les différents en-tete
line_pattern = re.compile(
    r'^(?P<time>\d{2}:\d{2}:\d{2}\.\d+)\s+'
    r'(?P<proto>IP|IP6)\s+'
    r'(?P<src>\S+)\s+>\s+'
    r'(?P<dst>\S+):\s*(?P<rest>.*)'
)

#analyser le reste de l'en-tete
def extract_optional(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else ""

#séparer l'IP et le Port
def split_ip_port(value):

    parts = value.rsplit(".", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return value, ""

# Supprime l'ancien CSV si il y a
for f in (OUTPUT_CSV, ANALYSE_CSV):
    if os.path.exists(f):
        os.remove(f)

#Compte les différentes IP sources
ip_source_count = defaultdict(int)

#ouverture du tcpdump et creation du premier csv
with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f, \
     open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
    #initie l'écriture du csv
    writer = csv.writer(csvfile, delimiter=";")

    # En-tête CSV
    writer.writerow([
        "Heure",
        "Protocole",
        "IP_source",
        "Port_source",
        "IP_destination",
        "Port_destination",
        "Flags",
        "Seq",
        "Ack",
        "Taille"
    ])

    for line in f:
        # Ignorer les lignes hexadécimales
        if line.startswith("\t") or line.startswith(" "):
            continue
    # Ignore les trames qui ne correspondent pas au reste
        match = line_pattern.match(line)
        if not match:
            continue

        #recupere le reste de l'entete
        rest = match.group("rest")

        #separe IP/port
        src_ip, src_port = split_ip_port(match.group("src"))
        dst_ip, dst_port = split_ip_port(match.group("dst"))

        # Comptage IP source
        ip_source_count[src_ip] += 1

        #Ecrire la ligne dans le CSV
        writer.writerow([
            match.group("time"),
            match.group("proto"),
            src_ip,
            src_port,
            dst_ip,
            dst_port,
            extract_optional(r'Flags\s+\[([^\]]+)\]', rest),
            extract_optional(r'seq\s+([^,]+)', rest),
            extract_optional(r'ack\s+(\d+)', rest),
            extract_optional(r'length\s+(\d+)', rest),
        ])
#Creation deuxieme CSV
with open(ANALYSE_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["IP_source", "Nombre_de_trames"])
    #Comptage et triage des IP source
    for ip, count in sorted(ip_source_count.items(), key=lambda x: x[1], reverse=True):
        writer.writerow([ip, count])
