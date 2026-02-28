import pyautogui
from pynput import mouse
import time
import pyperclip
import json
import re
import pandas as pd
from bs4 import BeautifulSoup
from pynput.mouse import Controller
import random
import math



def is_polynomial_valid(polynomial, point1, point2, point3, screen_width, screen_height):
    x_values = sorted([point1[0], point2[0], point3[0]])
    for x in range(x_values[0], x_values[2] + 1):
        y = round(polynomial(x))
        if y < 0 or y >= screen_height:
            return False
    return True

def polynomial_through_3points(point1, point2, point3, screen_width, screen_height):
    start_time = time.time()
    
    while True:
        x1, y1 = point1
        x2, y2 = point2
        x3, y3 = point3

        def polynomial(x):
            L1 = ((x - x2) * (x - x3)) / ((x1 - x2) * (x1 - x3))
            L2 = ((x - x1) * (x - x3)) / ((x2 - x1) * (x2 - x3))
            L3 = ((x - x1) * (x - x2)) / ((x3 - x1) * (x3 - x2))

            y = y1 * L1 + y2 * L2 + y3 * L3
            return y

        if is_polynomial_valid(polynomial, point1, point2, point3, screen_width, screen_height):
            return polynomial

        # Perturber légèrement le point2
        point2 = (point2[0], point2[1] + random.randint(-5, 5))
        
        # Si la recherche dépasse 5 secondes
        if time.time() - start_time > 5:
            print("NORMALED")
            x_values = sorted([point1[0], point2[0], point3[0]])
            return normalize_to_screen(polynomial, range(x_values[0], x_values[2] + 1), screen_width, screen_height,point1)


def normalize_to_screen(polynomial, x_range, screen_width, screen_height, start_point):
    # Évaluez le polynôme sur la plage x pour trouver les valeurs y min et max
    y_values = [polynomial(x) for x in x_range]
    y_min = min(y_values)
    y_max = max(y_values)
    
    # Calculer l'écart entre la valeur y du point de départ et la valeur y du polynôme normalisé
    y_start_actual = polynomial(start_point[0])
    y_start_normalized = ((y_start_actual - y_min) / (y_max - y_min)) * (screen_height-50)
    offset = start_point[1] - y_start_normalized

    # Définissez la fonction de normalisation en fonction de screen_height et des valeurs y min et max
    def normalized_polynomial(x):
        y = polynomial(x)
        normalized_y = ((y - y_min) / (y_max - y_min)) * (screen_height-50) + offset
        return normalized_y

    return normalized_polynomial






def get_points_between_3points(point1, point2, point3, screen_width, screen_height):
    polynomial = polynomial_through_3points(point1, point2, point3, screen_width, screen_height)
    
    x_values = list(range(point1[0], point3[0] + 1))
    points = [(point1[0], point1[1])]
    
    for x in x_values[1:-1]:  # Excluez le premier et le dernier x pour ajouter les points exacts plus tard
        y = round(polynomial(x))
        y_clamped = clamp(y, 0, screen_height-1)
        points.append((clamp(x, 0, screen_width-1), y_clamped))
    
    points.append((point3[0], point3[1]))  # Assurez-vous d'ajouter le dernier point exact
    return points

def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))

def get_adjusted_points(points, screen_width, screen_height):
    adjusted_points = []
    for x, y in points:
        adjusted_x = clamp(x, 0, screen_width-100)
        adjusted_y = clamp(y, 0, screen_height-100)
        adjusted_points.append((adjusted_x, adjusted_y))
    return adjusted_points

def move_mouse_pynput(path):
    if not path:
        return

    interpolated_path = [path[0]]

    for i in range(1, len(path)):
        interpolated_points = interpolate_points(path[i-1], path[i])
        interpolated_path.extend(interpolated_points[1:])

    for point in interpolated_path:
        mouse.position = point
        time.sleep(0.001)

def adjust_x_coordinate(pt, existing_x_coordinates):
    """Adjust x-coordinate of the point if it coincides with existing ones."""
    while pt[0] in existing_x_coordinates:
        pt = (pt[0] + random.choice([-1, 1]), pt[1])  # adjust x-coordinate by moving left or right
    return pt

def get_interpolated_points(start, end, n):
    # Cette fonction retourne une liste de n points entre start et end.
    x_spacing = (end[0] - start[0]) / (n + 1)
    y_spacing = (end[1] - start[1]) / (n + 1)

    points = []
    for i in range(1, n + 1):
        points.append((start[0] + i * x_spacing, start[1] + i * y_spacing))
    return points

def interpolate_points(start, end, max_distance=50):
    points = [start]
    
    distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    
    if distance <= max_distance:
        return [start, end]
    
    number_of_points = int(distance / max_distance)
    
    for i in range(1, number_of_points):
        interpolated_x = start[0] + i * (end[0] - start[0]) / number_of_points
        interpolated_y = start[1] + i * (end[1] - start[1]) / number_of_points
        points.append((int(interpolated_x), int(interpolated_y)))
    
    points.append(end)
    return points


def calculate_distance(point1, point2):
    """Calcule la distance euclidienne entre deux points."""
    return ((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)**0.5

def fake_navigation(point_final, screen_width, screen_height):
    fake_final_points = []
    existing_x_coordinates = [mouse.position[0]]
    all_pts = []
    
    # Générer des points finaux fictifs
    for i in range(0, 3):
        fake_point = (random.randint(0, screen_width), random.randint(0, screen_height))
        fake_point = adjust_x_coordinate(fake_point, existing_x_coordinates)
        fake_final_points.append(fake_point)
        existing_x_coordinates.append(fake_point[0])

    start_point = mouse.position

    # Pour chaque point fictif
    for j in fake_final_points:
        middle_point = (random.randint(min(start_point[0], j[0]), max(start_point[0], j[0])),
                        random.randint(min(start_point[1], j[1]), max(start_point[1], j[1])))
        middle_point = adjust_x_coordinate(middle_point, existing_x_coordinates)
        existing_x_coordinates.append(middle_point[0])

        points = get_points_between_3points(start_point, middle_point, j, screen_width, screen_height)
        all_pts.extend(points)
        start_point = j  # Le dernier point devient le point de départ pour la prochaine trajectoire

    # Pour le point final
    middle_point = (random.randint(min(start_point[0], point_final[0]), max(start_point[0], point_final[0])),
                    random.randint(min(start_point[1], point_final[1]), max(start_point[1], point_final[1])))
    middle_point = adjust_x_coordinate(middle_point, existing_x_coordinates)
    
    point_final = adjust_x_coordinate(point_final, existing_x_coordinates)
    final_points = get_points_between_3points(start_point, middle_point, point_final, screen_width, screen_height)
    all_pts.extend(final_points)
    
    # Enfin, déplacez la souris sur tous les points
    move_mouse_pynput(all_pts)


def create_link(prelink,indice_page):
    base_url = prelink.rsplit("page=", 1)[0]
    updated_url = base_url + "page=" + str(indice_page)
    print(updated_url)
    return updated_url

def click_on_link_bar():
    screen_width, screen_height = pyautogui.size()
    linkbar = (1242,75)
    try :
        fake_navigation(linkbar,screen_width,screen_height)
    except ZeroDivisionError:
            pass
    #x_link_bar = 1242
    #y_link_bar = 75

    
    pyautogui.click(1242,75)

def manipulate_linkbar(link_str):
    pyperclip.copy(link_str)

    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
   
    pyautogui.hotkey('ctrl', 'u')
    content_point = (1242,300)
    random_base_point = (random.randint(0,screen_width),random.randint(0,screen_height))
    x_link_bar = 1242
    y_link_bar = 300

    try :
        fake_navigation(content_point,screen_width,screen_height)
    except ZeroDivisionError:
        pass
        
    #pyautogui.click(x_link_bar, y_link_bar)
    
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    content = pyperclip.paste()
    pyautogui.hotkey('ctrl', 'w')
    try :
        fake_navigation(random_base_point,screen_width,screen_height)
    except ZeroDivisionError:
        pass
    #print(content)
    return content

def write_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


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
        #print(path)
    return html_path_list 

def create_JSON_path_list(pre_path,maxpages):
    json_path_list =[]
    pre_path = double_backslashes(pre_path)
   
    for i in range(1,maxpages+1):
        page_str= "\\page"
        page_str = double_backslashes(page_str)
        path = pre_path + page_str+str(i)+'.json'
        json_path_list.append(path)
        #print(path) 
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

    
        try :
            items_list = list(data['props']['pageProps']['initialProps']['searchData']['ads'])
        except KeyError:
            print("ERREUR RECUP PAGE")
            return 0
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
            try :
                item_data["Prix"] = (item['price'])[0]
            except KeyError:
                pass 
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
    
def export_data_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file_json:
        content= file_json.read()

        data = json.loads(content)

    

        try :
            items_list = list(data['props']['pageProps']['initialProps']['searchData']['ads'])
        except KeyError:
            print("ERREUR RECUP PAGE")
            return
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
        
          
        
            
        
            
        
            "Localisation":None,
        
            "Options de mise en valeur de l'annonce":[],

            


        
     




        }
    
        output_data = []

        for item in items_list:

        
            item_data["Titre de l'annonce"] = item['subject']
      
            item_data["Date publication"] = item['first_publication_date']
            item_data["Statut"] = item['status']
            item_data["Lien"] = item['url']
            try :
                item_data["Prix"] = (item['price'])[0]
            except KeyError:
                pass
            item_data["id de l'annonce"] = item['list_id']
      
            item_data["Localisation"] = item['location']
            item_str = str(item)
            item_data["Etat du produit"] = extract_value_from_key(item_str,'condition')
            item_data["Livraison"] =  extract_value_from_key(item_str,'shippable')
            item_data["Ancien prix"] =  extract_value_from_key(item_str,'old_price')
            
            item_data["Options de mise en valeur de l'annonce"] = item['options']

            print(item_data["Titre de l'annonce"])
        
        

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
        
            
        
            "Localisation":None,
        
            "Options de mise en valeur de l'annonce":[],
        
        
            }
        #print(output_data)


    return output_data

def export_data_multi(file_path):
    with open(file_path, 'r', encoding='utf-8') as file_json:
        content= file_json.read()

        data = json.loads(content)

    

        try :
            items_list = list(data['props']['pageProps']['initialProps']['searchData']['ads'])
        except KeyError:
            print("ERREUR RECUP PAGE")
            return
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

            "Image ou Son":None,

            "Produit":None,
        
          
        
            
        
            
        
            "Localisation":None,
        
            "Options de mise en valeur de l'annonce":[],

            


        
     




        }
    
        output_data = []

        for item in items_list:

        
            item_data["Titre de l'annonce"] = item['subject']
      
            item_data["Date publication"] = item['first_publication_date']
            item_data["Statut"] = item['status']
            item_data["Lien"] = item['url']

            try :
                item_data["Prix"] = (item['price'])[0]
            except KeyError:
                pass
            item_data["id de l'annonce"] = item['list_id']
      
            item_data["Localisation"] = item['location']
            item_str = str(item)
            item_data["Etat du produit"] = extract_value_from_key(item_str,'condition')
            item_data["Livraison"] =  extract_value_from_key(item_str,'shippable')
            item_data["Ancien prix"] =  extract_value_from_key(item_str,'old_price')
            item_data["Image ou Son"] =  extract_value_from_key(item_str,'image_sound_type_of_product')
            item_data["Produit"] =  extract_value_from_key(item_str,'image_sound_product')
            
            item_data["Options de mise en valeur de l'annonce"] = item['options']

            print(item_data["Titre de l'annonce"])
        
        

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

            "Image ou Son":None,

            "Produit":None,
        
          
        
            
        
            
        
            "Localisation":None,
        
            "Options de mise en valeur de l'annonce":[],
        
        
            }
        #print(output_data)


    return output_data

def export_all_data(json_list, maxpages):
    final_data = []
    for i in range(0, maxpages):
        print(i)
        if export_data(json_list[i]) != 0 :
            final_data += export_data(json_list[i])
            #final_data += export_data_multi(json_list[i])
            #final_data += export_data_info(json_list[i])

    data_frame = pd.DataFrame(final_data)
    
    # Suppression des doublons basés sur "id de l'annonce"
    data_frame = data_frame.drop_duplicates(subset="id de l'annonce", keep='first')
    #data_frame.to_excel('C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\ETUDES\\MULTIMEDIA\\Multimedia18.xlsx', index=False)
    data_frame.to_excel('C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\ETUDES\\ELECTROMENAGER\\Petit_Electromenager38.xlsx', index=False)
    #data_frame.to_excel('C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\ETUDES\\INFORMATIQUE\\Informatique19.xlsx', index=False)

screen_width, screen_height = pyautogui.size()

def get_all_html(max_pages):
    links = []
    cpt = 0
    i_start = 25
    html_list = create_HTML_path_list('C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\PAGES\\HTML',max_pages)
    json_list = create_JSON_path_list('C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\PAGES\\JSON',max_pages)
    for i in range(1,max_pages+1):
        #INFORMATIQUE LINK EN DESSOUS
        #links.append(create_link("https://www.leboncoin.fr/recherche?category=15&lat=48.9347346&lng=2.8837386&radius=100000&shippable=1&sort=time&item_condition=1%2C2&price=50-max&page=1",i))
        #MULTIMEDIA LINK EN DESSOUS
        #links.append(create_link("https://www.leboncoin.fr/recherche?category=16&lat=48.9347346&lng=2.8837386&radius=100000&shippable=1&sort=time&image_sound_product=videoprojecteur%2Chomecinema%2Cappareilsphotoobjectifs%2Ccamera%2Cdrone%2Cenceinte%2Ccasque&item_condition=1%2C6%2C2&page=1",i))
        #ELECTROMENAGER LINK EN DESSOUS
        links.append(create_link("https://www.leboncoin.fr/recherche?category=20&locations=r_12&owner_type=private&sort=time&item_condition=1%2C6%2C2%2C3&home_appliance_product=brosseadentelectrique%2Cbrossecoiffante%2Cepilateur%2Cferaboucler%2Clisseur%2Cpesepersonne%2Crasoirelectrique%2Csechecheveux%2Ctondeuse%2Cappareildecuisson%2Cbalancedecuisine%2Cbouilloire%2Cextracteurdejus%2Cgrillepain%2Cmachineacafe%2Cmachineapain%2Cmachineasoda%2Cmachineathe%2Crobotcuiseur%2Crobotmultifonction%2Crobotpatissier%2Cautresrobots%2Csorbetiere%2Ctireuseabiere%2Cyaourtiere%2Caspirateur%2Ccentralevapeur%2Ccentrederepassage%2Cdefroisseur%2Cferarepasser%2Cmachineacoudre%2Cnettoyeurvapeur%2Cventilateur&price=40-300&page=1",i))
    for link in links:
        
        print(link)
        click_on_link_bar()
        content = manipulate_linkbar(link)
        write_to_file(html_list[cpt],content)
        cpt = cpt+1
    from_html_list_to_json_list(html_list,json_list,max_pages)
    export_all_data(json_list,max_pages)
mouse = Controller()


json_list = create_JSON_path_list('C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\PAGES\\JSON',98)
#from_html_list_to_json_list(html_list,json_list,4)
#export_all_data(json_list,100)
#link_str = create_link("https://www.leboncoin.fr/recherche?category=20&item_condition=1%2C6%2C2%2C3&home_appliance_product=appareildemassage%2Cbrosseadentelectrique%2Cbrossecoiffante%2Cepilateur%2Cferaboucler%2Clisseur%2Cpesepersonne%2Crasoirelectrique%2Csechecheveux%2Ctondeuse%2Cautres%2Cappareildecuisson%2Cbalancedecuisine%2Cbarbecueetplanchaelectrique%2Cbouilloire%2Ccaveavin%2Ccuisiniere%2Cextracteurdejus%2Cfouramicroondes%2Cgaziniere%2Cgrillepain%2Cmachineacafe%2Cmachineapain%2Cmachineasoda%2Cmachineathe%2Cpianodecuisson%2Cplaquedecuisson%2Crobotcuiseur%2Crobotmultifonction%2Crobotpatissier%2Cautresrobots%2Csorbetiere%2Ctireuseabiere%2Cyaourtiere%2Caspirateur%2Ccentralevapeur%2Ccentrederepassage%2Cchauffagedappoint%2Cclimatiseur%2Cdefroisseur%2Cferarepasser%2Cmachineacoudre%2Cnettoyeurvapeur%2Cventilateur&price=40-300&page=1",1)

#click_on_link_bar()
get_all_html(98)
#manipulate_linkbar(link_str)

#extract_next_data_to_json("C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\PAGES\\DEBUG HTML\\informatique.html","C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\PAGES\\DEBUG JSON\\informatique.json")
