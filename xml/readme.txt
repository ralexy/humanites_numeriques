Afin de faire fonctionner notre application sur votre machine, veuillez suivre ces instructions :

1 - Lancer un serveur BaseX. Sur windows, il suffit simplement de cliquer sur l'icône "Basex http server (start)" dans le menu démarrer. Sur linux, il faudra exécuter le script basexserver.bat.
2 - Lancer le client BaseX. Sur windows, il suffit simplement de cliquer sur l'icône "Basex Client" dans le menu démarrer et d'entrer l'id "admin" et mot de passe "admin. Sur linux, il faudra exécuter le script basexclient.bat.

Je vous renvoie vers ce lien pour plus de détails concernant le lancement d'un serveur BaseX : https://docs.basex.org/wiki/Database_Server

Le serveur Basex sera lancé sur http://localhost:8984/rest/<Nom_de_votre_base_de_données>

3 - Installer python, ainsi que le gestionnaire de dépendances pip : https://geekflare.com/fr/python-pip-installation/
4 - Installer le framework python léger Flask via pip : pip install Flask
5 - Vous devrez modifier la valeur de la variable url à la ligne 14 dans le fichier flaskr/recherche.py dans le projet et la remplacer par le lien vers votre base de données BaseX : http://localhost:8984/rest/<Nom_de_votre_base_de_données>
6 - Se placer dans le répertoire du projet et lancer les commandes suivantes :

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

7 - le serveur web sera lancé sur http://localhost:5000 où vous pourrez tester notre application.
