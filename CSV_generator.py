import re
import csv

INPUT_FILE = "DumpFile.txt"
OUTPUT_CSV = "resultats.csv"

# Ligne principale d'une trame
line_pattern = re.compile(
    r'^(?P<time>\d+:\d+:\d+\.\d+)\s+'
    r'(?P<proto>\w+)\s+'
    r'(?P<src>[^ ]+)\s+>\s+'
    r'(?P<dst>[^:]+):\s*(?P<rest>.*)'
)

def extract_optional(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else ""

def split_ip_port(value):
    """
    Sépare IP et port.
    Exemple:
      BP-Linux8.ssh  -> IP=BP-Linux8  Port=ssh
      192.168.1.10.443 -> IP=192.168.1.10 Port=443
    """
    parts = value.rsplit(".", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return value, ""

with open(INPUT_FILE, "r") as f, open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")

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
        match = line_pattern.match(line)
        if match:
            rest = match.group("rest")

            src_ip, src_port = split_ip_port(match.group("src"))
            dst_ip, dst_port = split_ip_port(match.group("dst"))

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

print("✅ CSV structuré par colonnes, prêt pour Excel")
