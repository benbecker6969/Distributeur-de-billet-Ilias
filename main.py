import random
import datetime

# Variables
name = "BENHARRAT"
pinCode = "1207"
connectionAttempt = 0
accountBalance = random.uniform(1.0, 10000.0)
accountBalanceRounded: float = round(accountBalance, 2)
historyOfTheTransaction = []
accountBlocked = False
numberOfWithdrawals = 0
stockNumberToWithdraw = 0.0


# Fonction gestion d'erreur pour l'entrée du nombre à retirer
def TryFloat(value):
    try:
        return float(value)
    except ValueError:
        return 0.0


# Fonction de la connexion de l'utilisateur
def UserConnection():
    global connectionAttempt, accountBlocked
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
            print(
                "Compte bloqué ! Trop de tentatives de connexion ont été faites. Contacter votre conseiller bancaire.")
            accountBlocked = True


# Fonction qui permet de retirer
def Withdrawal():
    global accountBalanceRounded, numberOfWithdrawals, stockNumberToWithdraw
    while True:
        if numberOfWithdrawals > 5:
            print("Vous ne pouvez retirer plus de 5 fois par jour.")
            break
        inputAmount = input(f"Rentrez le montant que vous souhaitez retirer. Sachant que vous pouvez retirer maximum "
                            f"{200 - stockNumberToWithdraw:.2f}€ encore aujourd'hui: ")

        numberToWithdraw = TryFloat(inputAmount)
        if numberToWithdraw > 0:
            if stockNumberToWithdraw + numberToWithdraw > 200:
                print("Impossible de retirer plus de 200€ par jour !")
                break
            elif numberToWithdraw % 10 != 0:
                print("Montant invalide, il est impossible de retirer un nombre qui n'est pas un entier ou qui ne se "
                      "termine pas par 0 ou 5.")
            elif numberToWithdraw == 10:
                print("Impossible de retirer 10 euros, le distributeur ne propose pas de billets de 5 euros.")
            else:
                stockNumberToWithdraw += numberToWithdraw
                accountBalanceRounded = accountBalanceRounded - numberToWithdraw
                accountBalanceRounded = round(accountBalanceRounded, 2)

                quantityOfBill = int(input("Tapper 1 si vous souhaitez avoir le plus de billet possible\n"
                                           "Tapper 2 si vous souhaitez avoir le moins de billet possible : "))
                if quantityOfBill == 1:
                    BankNoteOfTen = numberToWithdraw // 10
                    RemainingAmount = numberToWithdraw % 10
                    if RemainingAmount > 0:
                        print(f"Vous avez reçu " + str(BankNoteOfTen) + " billets de 10 euros.")
                        print(f"Et {RemainingAmount:.2f}€ en espèces.")
                    else:
                        print(f"Vous avez reçu " + str(BankNoteOfTen) + " billets de 10 euros.")
                elif quantityOfBill == 2:
                    BankNoteOfFifty = numberToWithdraw // 50
                    RemainingAmount = numberToWithdraw % 50
                    if RemainingAmount > 0:
                        BankNoteOfTwenty = RemainingAmount // 20
                        RemainingAmount %= 20
                        BankNoteOfTen = RemainingAmount // 10
                        RemainingAmount %= 10
                        print(
                            "Vous avez reçu " + str(BankNoteOfFifty) + " billet(s) de 50 "
                                                                       "euros, " + str(
                                BankNoteOfTwenty) + " billet(s) de 20 euros "
                                                    "et " + str(BankNoteOfTen) + " billet(s) de 10 euros.")
                        if RemainingAmount > 0:
                            print(f"Et {RemainingAmount:.2f}€ en espèces.")
                    else:
                        print("Vous avez reçu " + str(BankNoteOfFifty) + " billet(s) de 50 euros.")
                else:
                    print("S'il vous plaît, entrer une option comprise entre 1 et 2. ")

                print(f'Vous venez de retirer {numberToWithdraw:.2f}€ avec succès.\nVoici votre nouveau solde: '
                      f'{accountBalanceRounded:.2f}€. vous pouvez retirer maximum '
                      f'{200 - stockNumberToWithdraw:.2f}€ encore aujourd\'hui.')
                currentDate = datetime.datetime.now()
                historyOfTheTransaction.append((currentDate.strftime("%Y-%m-%d %H:%M:%S"), numberToWithdraw))
                numberOfWithdrawals += 1
                break
        else:
            print("Le montant que vous avez rentrer est invalide.")


# Fonction qui affiche les 5 dernières transactions de l'utilisateur
def TransactionsHistory():
    if not historyOfTheTransaction:
        print("Vous ne possédez aucune transaction. Il est donc impossible de sortir un historique.")
    else:
        print("Voici vos dernières opération.\nIl faut savoir que le maximum de l'historique est de 5 opérations : "
              )
        for dateOfTransaction, amountOfTransaction, in historyOfTheTransaction[-5:]:
            dateOfTransactionReformed = datetime.datetime.strptime(dateOfTransaction, "%Y-%m-%d %H:%M:%S").strftime(
                "%d/%m/%Y %H:%M:%S")
            amountOfTransactionFormatted = "{:.2f}".format(amountOfTransaction)
            print("Le " + str(dateOfTransactionReformed) + " ,Vous avez retirer " +
                  amountOfTransactionFormatted + "€")


# Fonction qui permet à l'utilisateur de choisir le retrait, l'historique ou bien de partir
def UserChoice():
    global stockNumberToWithdraw
    while True:
        choiceOfUser = input("Pour retirer, tapper 1\nPour générer un reçu avec vos 5 dernières transactions, tapper 2"
                             "\nPour partir, tapper 3 : ")
        if choiceOfUser == "1":
            Withdrawal()
        elif choiceOfUser == "2":
            TransactionsHistory()
        elif choiceOfUser == "3":
            print("Merci beaucoup pour votre fidélité, XEFIBank vous souhaite une bonne journée !")
            break
        else:
            print("S'il vous plaît, entrer une option comprise entre 1 et 3.")


# Je rappel mes fonctions dans une boucle qui permet de bloqué l'utilisateur en cas de 3 essaie de connexion
while not accountBlocked:
    UserConnection()
    if accountBlocked:
        break
    UserChoice()
