import datetime
import sqlite3
import hashlib
import locale
from dateutil.parser import parse

locale.setlocale(locale.LC_TIME, "fr_FR.utf8")

# Variables
connectionAttempt = 0
accountBalanceRounded = 0.0
historyOfTheTransaction = []
accountBlocked = False
numberOfWithdrawals = 0
stockNumberToWithdraw = 0.0
username = ""
dailyWithdrawalLimit = 0.0

# Connection à ma BDD
conn = sqlite3.connect("xefibank.db")
cursor = conn.cursor()

current_datetime = datetime.datetime.now()

if current_datetime.time() == datetime.time(0, 0, 0):
    # Nombre de retrait et montant de retrait à 0 au bout de 00H00 dans ma BDD
    cursor.execute("UPDATE users SET daily_withdrawal_count = 0, daily_withdrawal_limit = 200.0")
    conn.commit()


# Fonction de conversion en float: gestion d'erreur
def TryFloat(value):
    try:
        return float(value)
    except ValueError:
        return 0.0


# Fonction de connexion de l'utilisateur
def UserConnection():
    global connectionAttempt, accountBlocked, accountBalanceRounded, username, dailyWithdrawalLimit

    while connectionAttempt < 3:
        username = input("Entrez votre nom d'utilisateur : ")
        pincode = input("Entrez votre Code Pin : ")

        with sqlite3.connect("xefibank.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                stored_password_hash = user[2]
                input_password_hash = hashlib.sha256(pincode.encode()).hexdigest()

                if input_password_hash == stored_password_hash:
                    accountBalanceRounded = user[6]
                    dailyWithdrawalLimit = user[4]

                    cursor.execute("SELECT date('now')")
                    current_date = cursor.fetchone()[0]
                    last_transaction_date = user[5]

                    print("Authentification réussie ! Bonjour {} !\nSolde : {:.2f}€.".format(username, accountBalanceRounded))
                    break
            else:
                print("Nom d'utilisateur ou mot de passe incorrect.")
                connectionAttempt += 1
                if connectionAttempt >= 3:
                    print(
                        "Le distributeur a été bloqué en raison d'un nombre excessif de tentatives de connexion "
                        "infructueuses.\n"
                        "Un message automatique a été envoyé à un conseiller qui arrivera"
                        " dans un délai maximal de 5 minutes pour débloquer le distributeur.")
                    accountBlocked = True
                    break

    if not accountBalanceRounded:
        with sqlite3.connect("xefibank.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT balance, daily_withdrawal_limit FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user:
                accountBalanceRounded = user[0]
                dailyWithdrawalLimit = user[1]


# Fonction qui permet de retirer
def Withdrawal():
    global accountBalanceRounded, numberOfWithdrawals, stockNumberToWithdraw, dailyWithdrawalLimit, username

    while True:
        if numberOfWithdrawals >= 5:
            print("Vous avez atteint la limite quotidienne de retraits (5 retraits par jour).")
            break

        if stockNumberToWithdraw is None:
            stockNumberToWithdraw = 0

        if stockNumberToWithdraw >= dailyWithdrawalLimit:
            print("Impossible,vous avez déjà retirer 200 € aujourd'hui.")
            break

        inputAmount = input(f"Rentrez le montant que vous souhaitez retirer. Sachant que vous pouvez retirer maximum "
                            f"{dailyWithdrawalLimit - stockNumberToWithdraw:.2f}€ encore aujourd'hui: ")

        numberToWithdraw = TryFloat(inputAmount)
        if numberToWithdraw > 0:
            if stockNumberToWithdraw + numberToWithdraw > dailyWithdrawalLimit:
                print("Montant invalide, vous ne pouvez pas retirer plus que votre limite quotidienne.")
            elif numberToWithdraw % 10 != 0:
                print("Montant invalide, il est impossible de retirer un nombre qui n'est pas un entier ou qui ne se "
                      "termine pas par 0 ou 5.")
            elif numberToWithdraw == 10:
                print("Impossible de retirer 10 euros, le distributeur ne propose pas de billets de 5 euros.")
            else:
                # Ajoute plus 1 à chaque retrait dans ma BDD
                cursor.execute("SELECT daily_withdrawal_count FROM users WHERE username = ?", (username,))
                current_count = cursor.fetchone()[0]

                if current_count >= 5:
                    print("Vous avez atteint la limite quotidienne de retraits (5 retraits par jour).")
                    break

                # Ajoute +1 à daily_withdrawal_count dans mon main.py
                new_count = current_count + 1
                stockNumberToWithdraw += numberToWithdraw
                remaining_limit = dailyWithdrawalLimit - stockNumberToWithdraw

                accountBalanceRounded = accountBalanceRounded - numberToWithdraw
                accountBalanceRounded = round(accountBalanceRounded, 2)

                cursor.execute("UPDATE users SET balance = ?, daily_withdrawal_limit = ?, daily_withdrawal_count = ? "
                               "WHERE username = ?",
                               (accountBalanceRounded, remaining_limit, new_count, username))
                conn.commit()

                currentDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO transactions (user_id, date, amount) VALUES ((SELECT id FROM users WHERE "
                               "username = ?), ?, ?)", (username, currentDate, numberToWithdraw))
                conn.commit()

                quantityOfBill = int(input("Tapez 1 si vous souhaitez avoir le plus de billets possible\nTapez 2 si "
                                           "vous souhaitez avoir le moins de billets possible : "))
                if quantityOfBill == 1:
                    BankNoteOfTen = numberToWithdraw // 10
                    RemainingAmount = numberToWithdraw % 10
                    if RemainingAmount > 0:
                        print(f"Vous avez reçu " + str(int(BankNoteOfTen)) + " billets de 10 euros.")
                        print(f"Et {RemainingAmount:.2f}€ en espèces.")
                    else:
                        print(f"Vous avez reçu " + str(int(BankNoteOfTen)) + " billets de 10 euros.")
                elif quantityOfBill == 2:
                    BankNoteOfFifty = numberToWithdraw // 50
                    RemainingAmount = numberToWithdraw % 50
                    if RemainingAmount > 0:
                        BankNoteOfTwenty = RemainingAmount // 20
                        RemainingAmount %= 20
                        BankNoteOfTen = RemainingAmount // 10
                        RemainingAmount %= 10
                        print("Vous avez reçu " + str(int(BankNoteOfFifty)) + " billet(s) de 50 euros, " + str(
                            int(BankNoteOfTwenty)) + " billet(s) de 20 euros " + "et " + str(
                            int(BankNoteOfTen)) + " billet(s) de 10 euros.")
                        if RemainingAmount > 0:
                            print(f"Et {RemainingAmount:.2f}€ en espèces.")

                print(
                    f'Vous venez de retirer {numberToWithdraw:.2f}€ avec succès.\nVoici votre nouveau solde: {accountBalanceRounded:.2f}€. vous pouvez retirer maximum {dailyWithdrawalLimit - stockNumberToWithdraw:.2f}€ encore aujourd\'hui.')
                historyOfTheTransaction.append((currentDate, numberToWithdraw))
                numberOfWithdrawals += 1
                break
        else:
            print("Le montant que vous avez rentré est invalide.")


# Fonction qui affiche les 5 dernières transactions de l'utilisateur
def TransactionsHistory():
    cursor.execute("SELECT date, amount FROM transactions WHERE user_id = (SELECT id FROM users WHERE username = ?) "
                   "ORDER BY date DESC LIMIT 5", (username,))
    user_transactions = cursor.fetchall()
    if not user_transactions:
        print("Vous ne possédez aucune transaction. Il est donc impossible de sortir un historique.")
    else:
        print("Voici vos dernières opérations. Le maximum que l'historique peut afficher est de 5 opérations : ")
        for dateOfTransaction, amountOfTransaction in user_transactions:
            dateOfTransactionParsed = parse(dateOfTransaction)
            dateOfTransactionFormatted = dateOfTransactionParsed.strftime("%d/%m/%Y %H:%M:%S")
            amountOfTransactionFormatted = "{:.2f}".format(amountOfTransaction)
            print("Le " + str(dateOfTransactionFormatted) + " ,Vous avez retiré " + amountOfTransactionFormatted + "€.")


# Fonction qui permet à l'utilisateur de choisir le retrait, l'historique ou bien de partir
def UserChoice():
    global stockNumberToWithdraw
    while True:
        cursor.execute("SELECT daily_withdrawal_count FROM users WHERE username = ?", (username,))
        current_count = cursor.fetchone()[0]

        remaining_withdrawals = 5 - current_count

        choiceOfUser = input(
            f"Vous avez encore {remaining_withdrawals} retrait(s) disponible(s) aujourd'hui.\nPour retirer, tapez "
            f"1\nPour générer un reçu avec vos 5 dernières transactions, tapez 2\nPour partir, tapez 3 : ")

        if choiceOfUser == "1":
            Withdrawal()
        elif choiceOfUser == "2":
            TransactionsHistory()
            locale.setlocale(locale.LC_TIME, "")
        elif choiceOfUser == "3":
            print("Merci beaucoup pour votre fidélité, XEFIBank vous souhaite une bonne journée !")
            break
        else:
            print("S'il vous plaît, entrez une option comprise entre 1 et 3.")


# Je rappelle mes fonctions dans une boucle qui permet de bloquer l'utilisateur en cas de 3 essais de connexion
while not accountBlocked:
    UserConnection()
    if accountBlocked:
        break
    UserChoice()
conn.close()
