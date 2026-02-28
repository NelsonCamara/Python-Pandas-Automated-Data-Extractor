# LeBonCoin Scraper

Un outil d'extraction et d'analyse de donnees pour les annonces LeBonCoin, avec simulation de comportement humain pour eviter la detection.

## Fonctionnalites

- **Scraping automatise** : Extraction des annonces depuis LeBonCoin avec pagination automatique
- **Simulation humaine** : Mouvements de souris realistes via interpolation polynomiale (courbes de Lagrange)
- **Extraction de donnees** : Parse les donnees JSON internes de LeBonCoin (`__NEXT_DATA__`)
- **Export Excel** : Generation de fichiers Excel avec suppression automatique des doublons
- **Multi-categories** : Support pour electromenager, multimedia, informatique

## Technologies

- **Python 3**
- **BeautifulSoup** - Parsing HTML
- **Pandas** - Traitement et export des donnees
- **PyAutoGUI** - Automatisation des interactions
- **Pynput** - Controle precis de la souris
- **Pyperclip** - Gestion du presse-papiers

## Structure du projet

```
src/
├── scrape_all.py       # Script principal de scraping complet
├── full_algo.py        # Pipeline d'extraction simplifie
├── human.py            # Simulation de mouvements humains
├── from_json.py        # Extraction des donnees JSON
├── get_pages.py        # Recuperation des pages HTML
├── to_json.py          # Conversion vers JSON
└── windows_automate.py # Automatisation Windows basique
```

## Installation

```bash
pip install beautifulsoup4 pandas pyautogui pynput pyperclip openpyxl
```

## Utilisation

### Scraping complet avec simulation humaine

```python
from scrape_all import get_all_html

# Scrape 10 pages d'annonces
get_all_html(10)
```

### Extraction de donnees uniquement

```python
from full_algo import export_all_data, create_JSON_path_list

json_list = create_JSON_path_list('chemin/vers/json', 10)
export_all_data(json_list, 10)
```

## Donnees extraites

Pour chaque annonce, les informations suivantes sont extraites :

| Champ | Description |
|-------|-------------|
| Titre de l'annonce | Nom du produit |
| Date publication | Date de mise en ligne |
| Prix | Prix actuel |
| Ancien prix | Prix avant reduction |
| Etat du produit | Neuf, Tres bon etat, etc. |
| Livraison | Disponibilite livraison |
| Localisation | Ville/Region |
| Marque | Marque du produit |
| Lien | URL de l'annonce |

## Algorithme de simulation humaine

Le module `human.py` implemente une simulation realiste des mouvements de souris :

1. **Interpolation polynomiale** : Utilise les polynomes de Lagrange pour creer des trajectoires courbes naturelles
2. **Points intermediaires aleatoires** : Genere des detours realistes avant d'atteindre la cible
3. **Normalisation** : Ajuste les trajectoires pour rester dans les limites de l'ecran
4. **Timing variable** : Delais aleatoires entre les actions

## Avertissement

Ce projet est fourni a des fins educatives uniquement. L'utilisation de scrapers peut violer les conditions d'utilisation de certains sites web. Utilisez de maniere responsable et respectez les robots.txt.

