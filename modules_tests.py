import unittest
import sys
import os

# Déterminer le répertoire du package TTT
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), 'TTT'))
print("Project root:", project_root)
tests_dir = os.path.join(project_root, 'tests')
print("Recherche des tests dans :", tests_dir)

# Ajouter project_root à sys.path pour que Python trouve le package TTT
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Trouver tous les fichiers de test disponibles
test_files = [
    f[:-3] for f in os.listdir(tests_dir) 
    if f.endswith('_test.py') and os.path.isfile(os.path.join(tests_dir, f))
]

if not test_files:
    print("Aucun test trouvé.")
    sys.exit(1)

# Afficher les options disponibles
print("\nModules de test disponibles :")
for i, test in enumerate(test_files, 1):
    print(f"{i}: {test}")

print("\nChoisissez les modules à tester (séparés par un espace).")
print("Laissez vide pour exécuter les modules sélectionnés. Tapez 'all' pour tout tester.")

# Sélection des modules
selected_modules = []
while True:
    user_input = input("> ").strip()
    
    if user_input.lower() == "all":
        selected_modules = test_files
        break
    elif user_input == "":
        if selected_modules:
            break
        print("Aucun module sélectionné. Veuillez entrer un choix ou 'all' pour tout tester.")
    else:
        selected_indexes = user_input.split()
        for index in selected_indexes:
            if index.isdigit() and 1 <= int(index) <= len(test_files):
                module_name = test_files[int(index) - 1]
                if module_name not in selected_modules:
                    selected_modules.append(module_name)
            else:
                print(f"Indice invalide : {index}. Réessayez.")

# Exécuter les tests sélectionnés
suite = unittest.TestSuite()
loader = unittest.TestLoader()

for module in selected_modules:
    suite.addTests(loader.discover(start_dir=tests_dir, pattern=f"{module}.py"))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Retourner un code d'erreur si un test a échoué
sys.exit(not result.wasSuccessful())
