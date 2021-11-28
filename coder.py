import re

def sub_chaine(patterns, repls, string):
	repls = list(repls)
	for pattern in patterns:
		string = re.sub(pattern, repls[0], string)
		repls.pop(0)
	return string

print("Entrez le code sous la forme d'une suite de lettre tout attaché:")
prop = input()
alphabet = "abcdefghijklmnopqrstuvw"

texte = input("Entrez le message : ").lower()

texte = re.sub("\W", " ", texte)
texte = re.sub("[0-9]", " ", texte)
texte = sub_chaine("éèùôàêâçîûïë", "eeuoaeaciuie", texte)

output = ""
for lettre in texte:
	if lettre == " ":
		output += " "
	else:
		index = alphabet.index(lettre)
		output += prop[index]

print()
print(output)