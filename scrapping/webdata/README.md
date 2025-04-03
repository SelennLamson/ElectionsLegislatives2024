# Données sur les candidats

Ces données correspondent à [l'article du monde](https://www.lemonde.fr/les-decodeurs/article/2024/07/01/la-carte-des-resultats-des-legislatives-au-premier-tour-et-le-tableau-des-candidats-qualifies_6245574_4355771.html) sur les élections. \
Il a été choisi de ne pas faire un scrap direct mais d'extraire l'HTML car cela permet de faire un historique des désistements. \
## Récupérer les données
Le fichier `data.html` correspond au tableau `#d_desist`.
Pour le récupérer, il suffit d'ouvrir la console: `Ctrl + Shift + I` ou simplement Clic-Droite -> inspecter l'élement puis d'aller dans la `console` puis de rentrer la commande suivante: 
```
document.querySelector('#d_desist')
```
il suffira de copier ce qui a été obtenu dans le fichier dans `data.html` \
