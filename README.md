# Gestionnaire de Compte Bancaire

Ce gestionnaire de compte bancaire est un programme Python simple conçu pour permettre aux utilisateurs de gérer leurs comptes, effectuer des retraits et consulter leur historique de transactions. Le code est prévu pour être utilisé en ligne de commande.

## Utilisation

1. Au démarrage, le programme invite l'utilisateur à s'authentifier en entrant son nom d'utilisateur et son code PIN. Par défaut, le nom d'utilisateur est "BENHARRAT" et le code PIN est "1207". L'utilisateur dispose de trois tentatives pour s'authentifier correctement.

2. Une fois l'authentification réussie, l'utilisateur peut choisir parmi plusieurs options :

   - Pour effectuer un retrait (dans la limite de 200€ par jour), l'option "1" permet à l'utilisateur de spécifier le montant à retirer ainsi que le choix entre le moins de billets possible (option "1") ou le plus de billets possible (option "2").

   - L'option "2" permet d'afficher un reçu contenant les détails des 5 dernières transactions. Si aucune transaction n'a été effectuée, un message indique que l'historique est vide.

   - Enfin, l'option "3" permet de quitter le programme.

3. Lorsqu'un utilisateur souhaite effectuer un retrait, le programme vérifie d'abord si le montant total retiré au cours de la journée n'excède pas 200€. Si c'est le cas, l'utilisateur est invité à indiquer le montant souhaité et à choisir entre le moins de billets possible ou le plus de billets possible. Le montant est ensuite déduit du solde du compte.

4. L'historique des transactions est conservé, et les 5 dernières transactions sont affichées si l'utilisateur le souhaite.

5. Notez que l'utilisateur est autorisé à effectuer un maximum de 5 retraits par jour. Une fois ce nombre atteint, il ne pourra plus effectuer de retraits jusqu'au jour suivant.

## Gestion des Erreurs

Ce programme a été amélioré pour gérer les erreurs d'entrée utilisateur de manière plus robuste. Par exemple :

- Si l'utilisateur entre un montant de retrait invalide (supérieur à 200€), le programme le guidera pour entrer une valeur valide.

- Si l'utilisateur choisit une option invalide, il sera invité à réessayer jusqu'à ce qu'une option valide soit choisie.

- Si l'utilisateur entre un nom d'utilisateur ou un code PIN incorrect à trois reprises, le compte sera bloqué, empêchant ainsi toute connexion ultérieure.

---

C'est ainsi que fonctionne ce gestionnaire de compte bancaire simple en Python. Il peut être utilisé pour simuler des opérations bancaires de base.
