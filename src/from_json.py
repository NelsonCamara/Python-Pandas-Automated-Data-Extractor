import json
import re
import pandas as pd



def extract_value_from_key(data_str, target_key):
    """
    Extrait une valeur associée à une clé donnée dans une chaîne brute.
    
    Paramètres:
        - data_str (str): La chaîne brute.
        - target_key (str): La clé dont la valeur doit être extraite.
    
    Retourne:
        - La valeur associée à la clé cible ou None si la clé n'est pas trouvée.
    """
    
    # Trouver la position de la clé
    key_pattern = f"{{'key': '{target_key}'"
    key_pos = data_str.find(key_pattern)
    if key_pos == -1:
        return None
    
    # Trouver la position de début de la valeur
    value_pattern = "'value_label': "
    start_pos = data_str.find(value_pattern, key_pos) + len(value_pattern)
    while data_str[start_pos] in [" ", "'"]:
        start_pos += 1

    # Trouver la position de fin de la valeur
    end_pos = data_str.find(",", start_pos)

    # Extraire la valeur
    value_str = data_str[start_pos:end_pos].strip().strip("'")

    return value_str

def export_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file_json:
        content= file_json.read()

        data = json.loads(content)

    

        items_list = list(data['props']['pageProps']['initialProps']['searchData']['ads'])
        #print(items_list[0]['condition'])

        item_data = {

            "Titre de l'annonce":None,

            "Date publication" :None,
        

            "Statut" :None,
        
        




        
            "Prix" :None,
        
            "Etat du produit":None,
        
            "id de l'annonce" :None,

            "Livraison":None,
        
            "Ancien prix":None,
        
            "Catégorie de produit":None,
        
            "Type de produit":None,
        
            "Marque":None,
        
            "Localisation":None,
        
            "Options de mise en valeur de l'annonce":[],
        
     




        }
    
        output_data = []

        for item in items_list:

        
            item_data["Titre de l'annonce"] = item['subject']
      
            item_data["Date publication"] = item['first_publication_date']
            item_data["Statut"] = item['status']
            item_data["Lien"] = item['url']
            item_data["Prix"] = item['price']
            item_data["id de l'annonce"] = item['list_id']
      
            item_data["Localisation"] = item['location']
            item_str = str(item)
            item_data["Etat du produit"] = extract_value_from_key(item_str,'condition')
            item_data["Livraison"] =  extract_value_from_key(item_str,'shippable')
            item_data["Ancien prix"] =  extract_value_from_key(item_str,'old_price')
            item_data["Catégorie de produit"] =  extract_value_from_key(item_str,'home_appliance_type')
            item_data["Type de produit"] =  extract_value_from_key(item_str,'home_appliance_product')
            item_data["Marque"] =  extract_value_from_key(item_str,'home_appliance_brand')
            item_data["Options de mise en valeur de l'annonce"] = item['options']

            print(item_data["Titre de l'annonce"],item_data["Marque"])
        
        

            #item_data["Titre de l'annonce"] = item['subject']
        

            output_data.append(item_data)

            item_data = {

            "Titre de l'annonce":None,

            "Date publication" :None,

            "Statut" :None,
        
        
        
            "Prix" :None,
        
            "Etat du produit":None,
        
            "id de l'annonce" :None,

            "Livraison":None,
        
            "Ancien prix":None,
        
            "Catégorie de produit":None,
        
            "Type de produit":None,
        
            "Marque":None,
        
            "Localisation":None,
        
            "Options de mise en valeur de l'annonce":[],
        
        
            }
        #print(output_data)



    data_frame =pd.DataFrame(output_data)
    data_frame.to_excel('Petit Electromenager2.xlsx', index=False)

file_path = 'C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\page1.json'


export_data(file_path)

