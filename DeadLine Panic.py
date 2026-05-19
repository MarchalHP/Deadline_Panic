import subprocess
import sys
import os
dossier_data = os.path.join(os.path.dirname(__file__), "Deadline_panic_data")
menu_path = os.path.join(dossier_data, "menu.py")
if not os.path.isfile(menu_path):
    print(f"[ERREUR] Impossible de trouver : {menu_path}")
    print("Vérifie que le dossier du projet est bien au bon endroit.")
    input("Appuie sur Entrée pour quitter...")
    sys.exit(1)
print("[LAUNCHER] Démarrage de DeadLine Panic...")
subprocess.run([sys.executable, menu_path])
