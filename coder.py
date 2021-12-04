# Programme utile pour coder son propre message à partir d'un code de chiffrement

import re

def sub_chaine(patterns, repls, string):
	repls = list(repls)
	for pattern in patterns:
		string = re.sub(pattern, repls[0], string)
		repls.pop(0)
	return string

# Chaque lettre de l'alphabet sera associé à la lettre donnée
print("Entrez le code de chiffrement sous la forme d'une suite de lettre tout attaché:")
prop = input()
alphabet = "abcdefghijklmnopqrstuvw"

texte = input("Entrez le message : ").lower()

texte = re.sub("\W", " ", texte)
texte = re.sub("[0-9]", " ", texte)
texte = sub_chaine("éèùôàêâçîûïë", "eeuoaeaciuie", texte)

# Génération
output = ""
for lettre in texte:
	if lettre == " ":
		output += " "
	else:
		index = alphabet.index(lettre)
		output += prop[index]

print()
print(output)
