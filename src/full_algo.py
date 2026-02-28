import pyautogui
from pynput import mouse
import time
import pyperclip
import json
import re
import pandas as pd
from bs4 import BeautifulSoup

def create_link(prelink,indice_page):
    base_url = prelink.rsplit("page=", 1)[0]
    updated_url = base_url + "page=" + str(indice_page)
    return updated_url

def click_on_link_bar():
    x_link_bar = 1242
    y_link_bar = 75

    
    pyautogui.click(x_link_bar, y_link_bar)

def manipulate_linkbar(link_str):
    pyperclip.copy(link_str)
    pyperclip.copy('')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    
    pyautogui.hotkey('ctrl', 'u')
    x_link_bar = 1242
    y_link_bar = 300

    
    pyautogui.click(x_link_bar, y_link_bar)
    time.sleep(2)

    pyautogui.hotkey('ctrl', 'a')
    
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.8)
    content = pyperclip.paste()
    pyautogui.hotkey('ctrl', 'w')

    print(content)
    return content

def write_to_file(path, content):
    with open(path, 'w') as file:
        file.write(content)
        file.close()

def double_backslashes(s):
    return s.replace('\\', '\\\\')

def create_HTML_path_list(pre_path,maxpages):
    html_path_list =[]
    pre_path = double_backslashes(pre_path)
 
    for i in range(1,maxpages+1):
        page_str= "\\page"
        page_str = double_backslashes(page_str)
        path = pre_path + page_str+str(i)+'.html'
        html_path_list.append(path)
        print(path)
    return html_path_list 

def create_JSON_path_list(pre_path,maxpages):
    json_path_list =[]
    pre_path = double_backslashes(pre_path)
   
    for i in range(1,maxpages+1):
        page_str= "\\page"
        page_str = double_backslashes(page_str)
        path = pre_path + page_str+str(i)+'.json'
        json_path_list.append(path)
        print(path) 
    return json_path_list



def extract_next_data_to_json(html_file_path, json_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
        
        if script_tag:
            json_content = script_tag.string
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json_file.write(json_content)
            print(f"Les données JSON ont été sauvegardées dans {json_file_path}")
        else:
            print("Balise <script id='__NEXT_DATA__'> non trouvée.")
                  
def from_html_list_to_json_list(html_list,json_list,maxpages):
    for i in range(0,maxpages):
        extract_next_data_to_json(html_list[i], json_list[i])

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
def remove_brackets(char_list):
    return [char for char in char_list if char not in ['[', ']']]

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
            item_data["Prix"] = (item['price'])[0]
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


    return output_data
    

def export_all_data(json_list,maxpages):
    final_data =[]
    for i in range(0,maxpages):
        final_data += export_data(json_list[i])
    data_frame =pd.DataFrame(final_data)
    data_frame.to_excel('Petit Electromenager4.xlsx', index=False)


html_list = create_HTML_path_list('C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\PAGES\\HTML',4)
json_list = create_JSON_path_list('C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\PAGES\\JSON',4)

#from_html_list_to_json_list(html_list,json_list,4)
export_all_data(json_list,4)
#link_str = create_link("https://www.leboncoin.fr/recherche?category=20&item_condition=1%2C6%2C2%2C3&home_appliance_product=appareildemassage%2Cbrosseadentelectrique%2Cbrossecoiffante%2Cepilateur%2Cferaboucler%2Clisseur%2Cpesepersonne%2Crasoirelectrique%2Csechecheveux%2Ctondeuse%2Cautres%2Cappareildecuisson%2Cbalancedecuisine%2Cbarbecueetplanchaelectrique%2Cbouilloire%2Ccaveavin%2Ccuisiniere%2Cextracteurdejus%2Cfouramicroondes%2Cgaziniere%2Cgrillepain%2Cmachineacafe%2Cmachineapain%2Cmachineasoda%2Cmachineathe%2Cpianodecuisson%2Cplaquedecuisson%2Crobotcuiseur%2Crobotmultifonction%2Crobotpatissier%2Cautresrobots%2Csorbetiere%2Ctireuseabiere%2Cyaourtiere%2Caspirateur%2Ccentralevapeur%2Ccentrederepassage%2Cchauffagedappoint%2Cclimatiseur%2Cdefroisseur%2Cferarepasser%2Cmachineacoudre%2Cnettoyeurvapeur%2Cventilateur&price=40-300&page=1",1)

#click_on_link_bar()

#manipulate_linkbar(link_str)
