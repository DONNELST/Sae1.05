import re
import csv
import os
from collections import defaultdict

# ==============================
# FICHIERS
# ==============================
INPUT_FILE = "DumpFile.txt"
OUTPUT_CSV = "resultats.csv"
ANALYSE_CSV = "analyse_ip_sources.csv"

# ==============================
# REGEX POUR LIGNES TCPDUMP
# ==============================
line_pattern = re.compile(
    r'^(?P<time>\d{2}:\d{2}:\d{2}\.\d+)\s+'
    r'(?P<proto>IP|IP6)\s+'
    r'(?P<src>\S+)\s+>\s+'
    r'(?P<dst>\S+):\s*(?P<rest>.*)'
)

# ==============================
# FONCTIONS UTILES
# ==============================
def extract_optional(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else ""

def split_ip_port(value):
    """
    Sépare IP et port :
    BP-Linux8.ssh            -> BP-Linux8 | ssh
    192.168.1.10.443         -> 192.168.1.10 | 443
    """
    parts = value.rsplit(".", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return value, ""

# ==============================
# SUPPRESSION DES CSV EXISTANTS
# ==============================
for f in (OUTPUT_CSV, ANALYSE_CSV):
    if os.path.exists(f):
        os.remove(f)

# ==============================
# COMPTEUR D'IP SOURCES
# ==============================
ip_source_count = defaultdict(int)

# ==============================
# TRAITEMENT DU TCPDUMP
# ==============================
with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f, \
     open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:

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

        match = line_pattern.match(line)
        if not match:
            continue

        rest = match.group("rest")

        src_ip, src_port = split_ip_port(match.group("src"))
        dst_ip, dst_port = split_ip_port(match.group("dst"))

        # Comptage IP source
        ip_source_count[src_ip] += 1

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

# ==============================
# ÉCRITURE DU CSV D'ANALYSE
# ==============================
with open(ANALYSE_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["IP_source", "Nombre_de_trames"])

    for ip, count in sorted(ip_source_count.items(), key=lambda x: x[1], reverse=True):
        writer.writerow([ip, count])

# ==============================
# FIN
# ==============================
print("✅ resultats.csv généré")
print("📊 analyse_ip_sources.csv généré")
