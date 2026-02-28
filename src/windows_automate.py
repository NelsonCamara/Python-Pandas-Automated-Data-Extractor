import pyautogui
from pynput import mouse
import time
import pyperclip




def on_click(x, y, button, pressed):
    if pressed:
        print(f'Cliqué aux coordonnées: x={x}, y={y}')
        # Arrêter le listener
        return False

# Créer et commencer le listener
#while (1):
#    with mouse.Listener(on_click=on_click) as listener:
#        listener.join()
#time.sleep(5)



# Coordonnées
#x_link_bar = 1242
#y_link_bar = 75

# Cliquer aux coordonnées spécifiées
#pyautogui.click(x_link_bar, y_link_bar)
time.sleep(3)
pyautogui.hotkey('ctrl', 'u')
time.sleep(1)


pyautogui.hotkey('ctrl', 'a')

# Simuler un Ctrl + C
pyautogui.hotkey('ctrl', 'c')

clipboard_content = pyperclip.paste()

print(clipboard_content)