import pyautogui
from pynput import mouse
import time
import pyperclip
import math
import ctypes
from pynput.mouse import Controller
import random


# Définition des fonctions

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
        time.sleep(0.004)


def fake_navigation2(point_final,screen_width,screen_height):
    fake_final_points =[]
    init_pts = []
    all_pts = []
    cpt = 0
    final_points =[]
    for i in range (0,3):
        fake_final_points.append((random.randint(0,screen_width),random.randint(0,screen_height)))
    for j in fake_final_points:
        if cpt >0:
            init_pts.append([(init_pts[cpt][0][0],init_pts[cpt][0][1]),(random.randint(mouse.position[0],fake_final_points[cpt][0]),random.randint(init_pts[cpt][0][0],init_pts[cpt][0][1])),fake_final_points[cpt]])

        init_pts.append([mouse.position,(random.randint(mouse.position[0],fake_final_points[cpt][0]),random.randint(mouse.position[1],fake_final_points[cpt][1])),fake_final_points[cpt]])
        points = get_points_between_3points(init_pts[cpt][0], init_pts[cpt][1],init_pts[cpt][2], screen_width, screen_height)
        all_pts.append(points)
        cpt = cpt+1
    final_points = get_points_between_3points((init_pts[cpt][0][0],init_pts[cpt][0][1]),(random.randint(init_pts[cpt][0][0],fake_final_points[2][0]),random.randint((init_pts[cpt][0][1],init_pts[cpt][2][1]))), point_final, screen_width, screen_height)
    all_pts.append(final_points)
    for parcours in all_pts:
        move_mouse_pynput(parcours)

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









# Programme principal

screen_width, screen_height = pyautogui.size()

# Initialisation de point1 à la position actuelle de la souris
mouse = Controller()
#point1 = mouse.position
#print(point1)
#point2 = (300, 75)
point3 = (1700, 800)
fake_navigation(point3,screen_width,screen_height)
#points = get_points_between_3points(point1, point2, point3, screen_width, screen_height)


#move_mouse_pynput(points)

