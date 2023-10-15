import sqlite3
import hashlib


def add_user_to_db(username, pincode, initial_balance):

    conn = sqlite3.connect("xefibank.db")
    cursor = conn.cursor()

    try:
        # Cryptage du mot de passe
        passwordEncrypt = hashlib.sha256(pincode.encode()).hexdigest()

        cursor.execute(
            "INSERT INTO users (username, pincode, initial_balance, daily_withdrawal_limit, daily_withdrawal_count, "
            "balance) VALUES (?, ?, ?, 200.0, 0, ?)",
            (username, passwordEncrypt, initial_balance, initial_balance))

        conn.commit()

        print(
            f"L'utilisateur {username} a été ajouté à la base de données avec un solde de {initial_balance}€.")
    except Exception as e:
        print("Une erreur a eu lieu lors de la création de l'utilisateur : ", str(e))
    finally:
        conn.close()


if __name__ == "__main__":
    username = input("Entrez le nom d'utilisateur : ")
    pincode = input("Entrez le code PIN : ")
    initial_balance = float(input("Entrez le solde initial : "))

    add_user_to_db(username, pincode, initial_balance)
