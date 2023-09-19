#  🖋️ Génération automatique de poèmes 🖋️
 Notre application permet de générer un poème à partir de mots de votre choix.     
 Vous pouvez en effet sélectionner 3 mots ainsi que la longueur souhaitée du poème.   
 Amusez-vous bien! 🎉

 Cette application a été créée par Yvan Belakebi-Joly, Vinciane Desbois, Simon Mariani & Clémence Millet dans le cadre de notre projet de Cloud Computing.

## Installation
 
Pour lancer le générateur de poème vous-même en local : 
```bash
git clone https://gitlab.com/ensae-dev/projects_2022_2023/poem-generation.git
```
Vérifiez que votre version de Python est ``python==3.9``.
```
pip install -r requirements.txt
flask run
```

Pour lancer le générateur de poème vous-même en version dockerisée :
```bash
docker pull simariani/poemgen:latest
docker run -d -p 5000:5000 simariani/poemgen:latest
````
Then click on http://localhost:5000/
## Méthodologie : 
Pour mettre au point notre générateur de poème, nous avons suivi les étapes suivantes : 

1. Scrapper les poèmes du site web : https://www.bonjourpoesie.fr  
2. Finetuner avec les poèmes scrappés un modèle préentrainé de génération de texte (T5)
3. Enregistrer ce modèle en ligne à l'aide d'HuggingFace
3. Créer l'application Flask
4. Tester l'application et le modèle à l'aide de tests unitaires
5. Dockériser notre application
6. Nous amuser à générer une infinité de poèmes 😄


## Détail des fichiers contenu dans le repository : 
1. **`data_factory` : Dossier qui contient les fichiers de traitement des données**
- `scrapping_poems.py` : script utilisé pour le scrapping de poème
- `webscrapped_poem_cleaning.py` : script utilisé pour nettoyer les poèmes issus du webscrapping
- `creation_keywords.py` : script qui créé le dataset d'entraînement à partir du webscrapping

2. **`model`: Dossier qui contient les fichiers de création et d'enregistrement du modèle**
- `config.json`: fichier contenant tous les paramètres du modèle T5
- `special_tokens_map.json`: fichier contenant des features du tokenizer du modèle
- `spiece.model` : fichier contenant des features du tokenizer du modèle
- `tokenizer_config.json` : fichier contenant tous les features du tokenizer du modèle
- `tokenizer.json` : fichier contenant des features du tokenizer du modèle
- `export_model_to_huggingface.py` : script permettant d'enregistrer le modèle sur HuggingFace
- `training.py`: script d'entraînement du modèle

3. **`static` : Dossier qui contient les éléments statiques de l'application**
- `style.css` : fichier CSS contenant les éléments de style utilisés dans les html
- `logo.png` : Image représentant le logo de l'application
- `small_logo_blue.png` : Image représentant le logo de l'application sans le texte

4. **`templates`: Dossier qui contient les templates html utiles pour l'application**
- `accueil.html` : html présentant la page d'accueil de l'application
- `selection_mots.html` : html permettant l'ajout des mots 
- `longueur_vers.html` : html permettant la sélection de la longueur du poème souhaité
- `generate_poem.html` : html qui affiche le poème généré

5. **`test`: Dossier contenant les tests unitaires**
- `test_app.py`: tests unitaires vérifiant les procédures de l'application flask
- `test_model.py`: tests unitaires vérifiant les sorties de la fonction de génération de poème

6. **`app.py` : script qui permet de lancer l'application avec flask**
7. **`Dockerfile` : fichier qui liste les instructions à exécuter pour build une image**
8. **`generation_t5.py` : script qui génère un poème à partir d'une liste de 3 mots**
9. **`requirements.txt` : librairies nécessaires pour la création de notre application de génération de poème**
10. **`.gitignore` : éléments que l'on ne souhaite jamais ajouter dans le repository Git**

## License
[MIT](https://choosealicense.com/licenses/mit/)
