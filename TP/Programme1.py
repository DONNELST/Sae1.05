# -*-coding: utf-8 -*
'''f = open('C:\\Users\\Admin\\Documents\\Sae1.05\\evenementSAE_15_2025.ics')
file = f.read()
champs = [ #servira plus tard
    "UID",
    "DATE",
    "HEURE",
    "DUREE",
    "MODALITE",
    "INTITULE",
    "SALLE",
    "PROF",
    "GROUPE"
]
lignes = file.splitlines()
contenu = {}

for ligne in file:
    ligne = ligne.strip()
    if ":" in ligne:
        cle, valeur = ligne.split(":", 1)
        contenu[cle] = valeur.strip()

print(contenu) #à corriger, ne retourne rien (retourne un dictionnaire mais sans les valeurs attendu)



'''

'''
entetes = [
     u'Colonne1',
     u'Colonne2',
     u'Colonne3',
     u'Colonne4',
     u'Colonne5'
]

valeurs = [
     [u'Valeur1', u'Valeur2', u'Valeur3', u'Valeur4', u'Valeur5'],
     [u'Valeur6', u'Valeur7', u'Valeur8', u'Valeur9', u'Valeur10'],
     [u'Valeur11', u'Valeur12', u'Valeur13', u'Valeur14', u'Valeur15']
]

f = open('C:\\Users\\Admin\\Documents\\Sae1.05\\evenementSAE_15_2025.ics', 'w')
ligneEntete = ";".join(entetes) + "\n"
f.write(ligneEntete)
for valeur in valeurs:
     ligne = ";".join(valeur) + "\n"
     f.write(ligne)

with open("C:\\Users\\Admin\\Documents\\Sae1.05\\monFichier.csv", "w") as f: 

    f.write(";".join(entetes) + "\n")
    for ligne in valeurs:
        f.write(";".join(ligne) + "\n")

f.close()'''

#la suite est fonctionnel : renvoie les valeurs dans un excel
import re

f = open("C:\\Users\\Admin\\Documents\\Sae1.05\\evenementSAE_15_2025.ics", "r")
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
with open("C:\\Users\\Admin\\Documents\\Sae1.05\\monFichier.csv", "w") as f: 

    f.write(";".join(entetes) + "\n")
    for ligne in valeurs:
        f.write(";".join(ligne) + "\n")

print("✔ CSV généré : monFichier.csv")