# Voir les caractères avec un accent dans le texte

import re
import string

file = open("texte_example", "r")
texte = file.read().lower()
file.close()

# Supprimer tous les caractères non-alphanumériques
texte = re.sub("\W", " ", texte)
texte = re.sub("[0-9]", " ", texte)
lettres = []
for lettre in texte:
	# Si la lettre n'a pas déjà été identifié et comporte bien un accent...
	if lettre not in lettres and lettre not in string.ascii_lowercase + " ":
		# ... alors l'ajouter à la liste
		lettres.append(lettre)

print(lettres)
