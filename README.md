# LeBonCoin Scraper

Un outil d'extraction et d'analyse de données pour les annonces LeBonCoin, avec simulation de comportement humain pour éviter la détection.

## Fonctionnalités

- **Scraping automatisé** : Extraction des annonces depuis LeBonCoin avec pagination automatique
- **Simulation humaine** : Mouvements de souris réalistes via interpolation polynomiale (courbes de Lagrange)
- **Extraction de données** : Parse les données JSON internes de LeBonCoin (`__NEXT_DATA__`)
- **Export Excel** : Génération de fichiers Excel avec suppression automatique des doublons
- **Multi-catégories** : Support pour électroménager, multimédia, informatique

## Technologies

- **Python 3**
- **BeautifulSoup** - Parsing HTML
- **Pandas** - Traitement et export des données
- **PyAutoGUI** - Automatisation des interactions
- **Pynput** - Contrôle précis de la souris
- **Pyperclip** - Gestion du presse-papiers

## Structure du projet

```
src/
├── scrape_all.py       # Script principal de scraping complet
├── full_algo.py        # Pipeline d'extraction simplifié
├── human.py            # Simulation de mouvements humains
├── from_json.py        # Extraction des données JSON
├── get_pages.py        # Récupération des pages HTML
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

### Extraction de données uniquement

```python
from full_algo import export_all_data, create_JSON_path_list

json_list = create_JSON_path_list('chemin/vers/json', 10)
export_all_data(json_list, 10)
```

## Données extraites

Pour chaque annonce, les informations suivantes sont extraites :

| Champ | Description |
|-------|-------------|
| Titre de l'annonce | Nom du produit |
| Date publication | Date de mise en ligne |
| Prix | Prix actuel |
| Ancien prix | Prix avant réduction |
| État du produit | Neuf, Très bon état, etc. |
| Livraison | Disponibilité livraison |
| Localisation | Ville/Région |
| Marque | Marque du produit |
| Lien | URL de l'annonce |

## Algorithme de simulation humaine

Le module `human.py` implémente une simulation réaliste des mouvements de souris :

1. **Interpolation polynomiale** : Utilise les polynômes de Lagrange pour créer des trajectoires courbes naturelles
2. **Points intermédiaires aléatoires** : Génère des détours réalistes avant d'atteindre la cible
3. **Normalisation** : Ajuste les trajectoires pour rester dans les limites de l'écran
4. **Timing variable** : Délais aléatoires entre les actions

## Avertissement

Ce projet est fourni à des fins éducatives uniquement. L'utilisation de scrapers peut violer les conditions d'utilisation de certains sites web. Utilisez de manière responsable et respectez les robots.txt.
