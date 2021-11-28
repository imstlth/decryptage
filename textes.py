# Classer les textes par taille

import requests
import bs4

# On récupère la liste des textes
requete = requests.get("http://abu.cnam.fr/BIB/")
# Si ça ne fonctionne pas sur windows, enlever features="lxml"
soupe = bs4.BeautifulSoup(requete.content, features="lxml")
livres = {}


for link in soupe.find_all("a"):

	href = link.get("href")
	# On vérifie que c'est bien un lien qui mène à un livre
	if href.startswith("/cgi-bin/go?"):
		title = link.string

		# On récupère l'information de la taille
		requete2 = requests.get("http://abu.cnam.fr/cgi-bin/donner?" + href[12:])
		soupe2 = bs4.BeautifulSoup(requete2.content, features="lxml")
		# Qui se trouve dans la première balise <b>
		phrase = soupe2.find_all("b")[0].string
		taille = int(phrase[20:-3])
		livres[title] = taille
		requete2.close()


# Classement par taille
def key(key):
	return livres[key]

print(sorted(livres, key=key))