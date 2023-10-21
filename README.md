# XEFIBank - Documentation

Bienvenue dans la documentation de XEFIBank, une application bancaire simple pour gérer vos transactions et effectuer des retraits. Ce document explique les différentes parties de l'application et comment les utiliser.

## Composants de XEFIBank

1. **main.py**
   Le fichier main.py est le cœur de l'application XEFIBank. Il gère l'authentification des utilisateurs, les retraits, l'affichage de l'historique des transactions et les interactions avec les comptes.

2. **Base de données SQLite (xefibank.db)**
   Le fichier xefibank.db est une base de données SQLite qui stocke les données des utilisateurs, telles que les noms d'utilisateur, les codes PIN, les soldes, les limites de retrait journalier et l'historique des transactions. La base de données comprend deux tables : users et transactions.

3. **API Flask**
   L'API Flask fournit des points de terminaison pour l'authentification des utilisateurs et les retraits. Elle permet à des applications ou services externes d'interagir avec le système XEFIBank. L'API dispose de deux points de terminaison principaux : /login pour l'authentification et /withdraw pour les retraits.

## Comment exécuter l'application XEFIBank

**Configuration de l'environnement :**

- Assurez-vous d'avoir Python installé sur votre système.
- Installez les packages Python requis en exécutant la commande suivante : `pip install Flask dateutil`.

**Exécution de l'API Flask :**

1. Ouvrez un terminal ou une invite de commande.
2. Naviguez jusqu'au répertoire contenant votre script d'API Flask (celui que vous avez fourni).
3. Lancez l'API Flask en exécutant le script à l'aide de la commande suivante :


**Exécution de main.py :**

1. Ouvrez un autre terminal ou une invite de commande.
2. Naviguez jusqu'au répertoire contenant main.py.
3. Exécutez le script en utilisant la commande suivante :

4. Suivez les invites pour interagir avec l'application XEFIBank.

## Fonctionnalités de XEFIBank

L'application XEFIBank offre les fonctionnalités suivantes :

- **Authentification des utilisateurs** : Les utilisateurs sont invités à saisir leur nom d'utilisateur et leur code PIN pour s'authentifier. Après trois tentatives infructueuses, le compte est temporairement bloqué.

- **Retraits** : Les utilisateurs peuvent effectuer des retraits, sous réserve de certaines règles. Ils ne peuvent retirer qu'un montant maximum par jour et effectuer un nombre limité de retraits par jour. Le programme calcule la manière la plus efficace de distribuer les billets pour le montant demandé.

- **Historique des transactions** : Les utilisateurs peuvent consulter les cinq dernières transactions effectuées.

- **API Flask** : Des applications ou services externes peuvent utiliser l'API Flask pour authentifier les utilisateurs et effectuer des retraits de manière programmatique.

## Notes importantes

- **Blocage du compte** : Après trois tentatives infructueuses d'authentification, le compte est bloqué temporairement.

- **Limites de retrait** : Les utilisateurs ne peuvent retirer qu'un montant limité par jour et effectuer un nombre limité de retraits.

- **Distribution des billets** : Le programme calcule la manière la plus efficace de distribuer les billets lorsque les utilisateurs effectuent un retrait, en tenant compte des dénominations de billets disponibles.
