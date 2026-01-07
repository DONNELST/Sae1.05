import re

INPUT_FILE = "DumpFile.txt"
OUTPUT_MD = "resultats.md"

# Détection générique d'une ligne de trame
line_pattern = re.compile(
    r'^(?P<time>\d+:\d+:\d+\.\d+)\s+'
    r'(?P<proto>\w+)\s+'
    r'(?P<src>[^ ]+)\s+>\s+'
    r'(?P<dst>[^:]+):\s*(?P<rest>.*)'
)

def extract_optional(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else ""

packets = []

with open(INPUT_FILE, "r") as f:
    for line in f:
        match = line_pattern.match(line)
        if match:
            rest = match.group("rest")

            packet = {
                "time": match.group("time"),
                "proto": match.group("proto"),
                "src": match.group("src"),
                "dst": match.group("dst"),
                "flags": extract_optional(r'Flags\s+\[([^\]]+)\]', rest),
                "seq": extract_optional(r'seq\s+([^,]+)', rest),
                "ack": extract_optional(r'ack\s+(\d+)', rest),
                "length": extract_optional(r'length\s+(\d+)', rest),
            }

            packets.append(packet)

with open(OUTPUT_MD, "w") as md:
    md.write("# Analyse générique du fichier Dump réseau\n\n")
    md.write("| Heure | Proto | Source | Destination | Flags | Seq | Ack | Taille |\n")
    md.write("|-------|-------|--------|-------------|-------|-----|-----|--------|\n")

    for p in packets:
        md.write(
            f"| {p['time']} | {p['proto']} | {p['src']} | {p['dst']} | "
            f"{p['flags']} | {p['seq']} | {p['ack']} | {p['length']} |\n"
        )

print("✅ Markdown généré sans dépendance à un hôte ou port")