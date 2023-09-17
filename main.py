import random

name = "BENHARRAT"
pinCode = "1207"
connectionAttempt = 0
accountBalance = random.uniform(1.0, 10000.0)
accountBalanceRounded = round(accountBalance, 2)

while connectionAttempt < 3:
    userName = input("Entrer votre nom d'utilisateur : ")
    writePinCode = input("Entrer votre Code Pin : ")

    if userName == name and writePinCode == pinCode:
        print("Votre authentification est valide ! Bonjour " + name + " !\nVotre solde est de " + str(
            accountBalanceRounded) + "€.")
        break
    else:
        print("Votre nom d'authentification ou bien votre mot de passe est incorrect.")
        connectionAttempt += 1

    if connectionAttempt == 3:
        print("Compte bloqué ! Trop de tentatives de connexion ont été faites. Contacter votre conseiller bancaire.")

# Utilisateur peut retirer un maximum de EUR 200 par jour ou le maximum de son solde si c'est moins que 200 EUR :
while True:
    choiceOfUser = input("Pour retirer, tapper 1.\nPour générer un reçu avec vos 5 dernières transactions, "
                         "tapper 2.\nPour partir, tapper 3 ")
    if choiceOfUser == "1":
        numberToWithdraw = float(input("Rentrer le montant que vous souhaiter retirer : "))
        if numberToWithdraw > 200:
            print("Impossible de retier plus de 200€ par jour !")
        else:
            accountBalanceRounded = accountBalanceRounded - numberToWithdraw
            print(
                "Vous venez de retier " + str(numberToWithdraw) + "€ avec succès.\n Voici votre nouveau solde : " + str(
                    accountBalanceRounded))
    elif choiceOfUser == "2":
        print("Voici vos dernières opération")
    elif choiceOfUser == "3":
        print("Merci beacoup pour votre fidélité, XEFI vous souhaite une bonne journée !")
        break
