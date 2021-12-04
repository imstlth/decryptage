# Décryptage d'un code par subsition à l'aide des Méthodes de Monte-Carlo par Chaînes Markov (avec l'algorithme de Métropolis)
# Vidéo à l'origine du projet :
# https://youtu.be/z4tkHuWZbRA

import re
import string
import matplotlib.pyplot as plt
import ast
import math
import random
import copy

# texte_example contient "Les Confessions" de Jean-Jacques Rousseau
# Livre disponible sur l'Association des Bibliophiles Universels (ABU)
# http://abu.cnam.fr/cgi-bin/donner?confessions1
# C'est le deuxième plus gros texte disponible sur l'ABU
# Voir avec "textes.py" qui classe les textes en fonction de leur taille

file = open("texte_example", "r")
texte = file.read().lower()
file.close()


# Création d'une fonction pour appliquer re.sub différemment
def sub_chaine(patterns, repls, string):
	repls = list(repls)
	for pattern in patterns:
		string = re.sub(pattern, repls[0], string)
		repls.pop(0)
	return string

# Suppression des caractères spéciaux et des chiffres
texte = re.sub("\W", " ", texte)
texte = re.sub("[0-9]", " ", texte)
texte = sub_chaine("éèùôàêâçîûïë", "eeuoaeaciuie", texte)


alphabet = string.ascii_lowercase + " "
# * 27 car il y a 26 lettres dans l'alphabet + l'espace
stats = [[0] * 27] * 27
# En fait, l'instruction au dessus crée une liste de "références" (notion que je ne maîtrise pas du tout)
# Ainsi, j'utilise le module ast.literal_eval qui transforme un str en ce qu'il représente :
# Exemple :
# >>> a = "[0, 1]"
# >>> print(a)
# "[0, 1]"
# >>> a = ast.literal_eval(a)
# >>> print(a)
# [0, 1]
# Combiné avec repr(), ça crée une copie très superficielle.
stats = ast.literal_eval(repr(stats))


n = 0
# texte[:-1] car sinon il y a aurait un problème avec alphabet.index(texte[n + 1]). En effet, à la fin n + 1 serait plus grand que la taille de texte
for lettre in texte[:-1]:
	# Les lignes sont les lettres qui viennent en premier
	# Les colonnes sont les lettres qui suivent
	avant = alphabet.index(lettre)
	apres = alphabet.index(texte[n + 1])
	# Il y a forcément des endroits avec deux espaces et il ne faut pas les compter.
	if lettre == " " and texte[n + 1] == " ":
		pass
	else:
		stats[avant][apres] += 1
	n += 1


# On peut aussi transformer le tableau en pourcentage
# Mais je ne pense pas que ce soit une bonne idée
pourcent_stats = [] # À remplacer par [] si on veut les pourcentages
for ligne in stats:
	pourcent_stats.append([])
	somme = sum(ligne)
	for colonne in ligne:
		pourcent_stats[-1].append(colonne / somme * 100)


# Afficher le tableau avec matplotlib
fig, ax = plt.subplots()
ax.imshow(pourcent_stats, cmap=plt.get_cmap("plasma"))
# Je me suis pas mal aidé de la doc de matplotlib pour cette partie
# Car je voulais afficher les lettres
ax.set_xticks(list(range(27)))
ax.set_yticks(list(range(27)))
ax.set_xticklabels(alphabet)
ax.set_yticklabels(alphabet)

plt.show()


##########
# Seconde partie
##########


print("Entrez le texte :")
entree = input("").lower()

entree = re.sub("\W", " ", entree)
entree = re.sub("[0-9]", " ", entree)
entree = sub_chaine("éèùôàêâçîûïë", "eeuoaeaciuie", entree)


# Définition de la fonction qui permet d'obtenir le score pour un texte
def get_score(text):
	n = 0
	score = 1
	for lettre in text[:-1]: # De nouveau sinon n+1 serait plus grand que la taille du texte
		# J'ai pas tout compris lorsqu'il parle de la formule à 6:44 mais j'ai essayé de faire de mon mieux
		avant = alphabet.index(lettre)
		apres = alphabet.index(text[n + 1])
		# Ne pas compter les doubles espaces
		if lettre == " " and text[n + 1] == " ":
			pass
		# Ne pas compter si c'est égal à 0 car ça faire que le score total est égal à 0
		elif pourcent_stats[avant][apres] != 0:
			score *= pourcent_stats[avant][apres]
		n += 1

	# Je pense que c'est ça "normaliser par le nombre de caractère"
	return math.log(score) / len(text)

print("""
Plausibilité du texte entré : """ + str(get_score(entree)))

# Création d'une proposition intiale en analysant les fréquences de lettres
freq_texte = {}
freq_entree = {}

for lettre in alphabet[:-1]: # On enlève l'espace
	freq_texte[lettre] = texte.count(lettre) # D'un côté le texte d'example
	freq_entree[lettre] = entree.count(lettre) # D'un autre le texte d'entrée

def key_texte(key):
	return freq_texte[key]

def key_entree(key):
	return freq_entree[key]

# On les classe
sorted_freq_texte = sorted(freq_texte, key=key_texte)
sorted_freq_texte.reverse()
sorted_freq_entree = sorted(freq_entree, key=key_entree)
sorted_freq_entree.reverse()

# Création de la proposition
prop = {}
for lettre in alphabet[:-1]:
	index = sorted_freq_texte.index(lettre)
	prop[lettre] = sorted_freq_entree[index]

# Boucle principale
count = 0
while True:
	count += 1
	choix = []
	# On teste 60 permutations à la fois
	for permutation in range(60):
		# On choisit 2 lettres au hasard
		lettre1 = random.choice(alphabet[:-1])
		lettre2 = random.choice(alphabet[:-1])
		while lettre2 == lettre1:
			lettre2 = random.choice(alphabet[:-1])
		choix.append([lettre1, lettre2])

	plausibilites = []
	props = []
	sorties = []

	# Pour chaque permutation
	for test in choix:

		# Enregistrer la nouvelle proposition de déchiffrement
		new_prop = copy.copy(prop)
		new_prop[test[0]], new_prop[test[1]] = new_prop[test[1]], new_prop[test[0]]
		props.append(new_prop)
		new_entree = ""
		# On applique la proposition au texte d'entrée
		for lettre in entree:
			if lettre == " ":
				new_entree += " "
			else:
				new_entree += new_prop[lettre]
		# Et on enregistre la plausibilité associée
		plausibilites.append(get_score(new_entree))
		sorties.append(new_entree)
	
	index = plausibilites.index(max(plausibilites))
	prop = props[index]
	entree = sorties[index]

	if get_score(entree) >= 2.3:
		break

print("""
=====
Finis en %s opérations
=====
""" % str(count))
print("Texte décodé :")
print(entree)
print("""
Plausibilité du texte décodé : """ + str(get_score(entree)))
print("""
Code de déchiffrement :""")
print(" ".join(alphabet[:-1]))
print(" ".join(list(prop.values())))
