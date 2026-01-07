import csv
from collections import Counter

INPUT_FILE = "traffic.csv"
OUTPUT_FILE = "rapport.md"

packets = []
lengths = []
flags_counter = Counter()

with open(INPUT_FILE, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        packets.append(row)
        lengths.append(int(row["Length"]))
        flags_counter[row["Flags"]] += 1

with open(OUTPUT_FILE, "w") as md:
    md.write("# 📡 Rapport d’analyse du trafic réseau\n\n")

    md.write("## 📊 Statistiques générales\n")
    md.write(f"- **Nombre total de paquets** : {len(packets)}\n")
    md.write(f"- **Taille moyenne des paquets** : {sum(lengths)/len(lengths):.2f} octets\n\n")

    md.write("## 🚦 Répartition des Flags TCP\n")
    for flag, count in flags_counter.items():
        md.write(f"- `{flag}` : {count}\n")

    md.write("\n## 📋 Détails des paquets\n")
    md.write("| Heure | Source | Destination | Flags | Taille |\n")
    md.write("|------|--------|-------------|-------|--------|\n")

    for p in packets:
        md.write(f"| {p['Time']} | {p['Source']} | {p['Destination']} | {p['Flags']} | {p['Length']} |\n")

print("✅ Rapport Markdown généré → rapport.md")