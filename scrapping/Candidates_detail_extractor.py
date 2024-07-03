from bs4 import BeautifulSoup
import json
import requests

# Lire le contenu du fichier HTML
with open('webscrapping/webdata/formatted_data.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, 'html.parser').prettify()


# Trouver la div principale contenant les données
div_table = soup.find('div', class_='divTable', id='d_desist')

# Initialiser le dictionnaire des résultats
result = {}

# Parcourir les lignes du tableau
for ligne in div_table.find_all('div', class_='tableauLigne'):
    # Récupérer les éléments contenant les noms et les partis
    candidat_elements = ligne.select('.tableauCellule.flex.nom .candidat')
    parti_elements = ligne.select('.tableauCellule.parti .famille span')

    # Parcourir les candidats et leurs partis respectifs
    for i, candidat_element in enumerate(candidat_elements):
        # Récupérer le nom du candidat
        candidat_nom = candidat_element.get_text().strip().replace(
            '\u00a0', ' ').replace("\n", '')
        desist = candidat_element.find(
            'span', class_='desistement') is not None
        if desist:
            candidat_nom = candidat_nom.replace(' désist.', '').strip()

        # Récupérer le parti associé
        if i < len(parti_elements):
            parti_nom = parti_elements[i].get_text().strip()
        else:
            parti_nom = parti_elements[0].get_text().strip()

        # Vérifier si le candidat est marqué comme désisté
        desist = candidat_element.find(
            'span', class_='desistement') is not None

        # Ajouter les informations du candidat au dictionnaire
        result[candidat_nom] = {"parti": parti_nom, "desist": desist}

with open('data/candidates_details.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)
print(result)
