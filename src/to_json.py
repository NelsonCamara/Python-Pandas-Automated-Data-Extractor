from bs4 import BeautifulSoup

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

# Remplacez par les chemins d'accès appropriés
html_file_path = 'C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\page1.html'
json_file_path = 'C:\\Users\\Nelson\\Documents\\Code_Nelson\\Leboncoin\\page1.json'
extract_next_data_to_json(html_file_path, json_file_path)
