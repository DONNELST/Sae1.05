import re

f = open("C:\\Users\\Admin\\Documents\\sae1.05\\Sae1.05\\ADE_RT1_Septembre2025_Decembre2025.ics", "r")
#Si on ne double pas les \, renvoie un warning (marche quand même)
contenu = f.read()

evenements = re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", contenu, re.DOTALL)

# Colonnes du CSV
entetes = [
    "DTSTART",
    "DTEND",
    "DUREE",
    "SUMMARY",
    "LOCATION",
    "DESCRIPTION"
]

# Liste pour stocker les lignes
valeurs = []

for evt in evenements:
    # Extraction de chaque champ
    def extraire(champ):
        match = re.search(rf"{champ}:(.*)", evt)
        return match.group(1).strip() if match else ""

    dtstart = extraire("DTSTART")
    dtend = extraire("DTEND")
    duree = int(dtend[9:12]) - int(dtstart[9:12])  #effectue la différencte entre la fin et le début pour donnée la durée
    summary = extraire("SUMMARY")
    location = extraire("LOCATION")
    description = extraire("DESCRIPTION").replace("\\n", " ").strip()

    valeurs.append([dtstart, dtend,"0"+str(duree)+"0", summary, location, description])

# -------- Écriture dans un fichier CSV --------
with open("C:\\Users\\Admin\\Documents\\Sae1.05\\monFichier2.csv", "w") as f: 

    f.write(";".join(entetes) + "\n")
    for ligne in valeurs:
        f.write(";".join(ligne) + "\n")

print("✔ CSV généré : monFichier.csv")