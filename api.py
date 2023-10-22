import hashlib

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Endpoint authentifiaction USER
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    pincode = data['pincode']

    conn = sqlite3.connect("xefibank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        stored_password_hash = user[2]
        input_password_hash = hashlib.sha256(pincode.encode()).hexdigest()

        if input_password_hash == stored_password_hash:
            account_balance = user[6]
            daily_withdrawal_limit = user[4]
            response = {
                "message": "Authentication successful.",
                "username": username,
                "account_balance": account_balance,
                "daily_withdrawal_limit": daily_withdrawal_limit
            }
            return jsonify(response), 200  # Authentification réussie
        else:
            response = {
                "message": "The password is incorrect."
            }
            return jsonify(response), 401  # Échec d'authentification
    else:
        response = {
            "message": "The user does not exist."
        }
        return jsonify(response), 404  # Utilisateur non trouvé

    conn.close()

# Endpoint pour les retrait
@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    username = data['username']
    amount = data['amount']

    conn = sqlite3.connect("xefibank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance, daily_withdrawal_limit, daily_withdrawal_count FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()

    if not user_data:
        conn.close()
        return jsonify({"message": "User not found"})

    account_balance = user_data[0]
    daily_withdrawal_limit = user_data[1]
    daily_withdrawal_count = user_data[2]

    if daily_withdrawal_count >= 5:
        conn.close()
        return jsonify({"message": "You have reached the daily withdrawal limit (5 withdrawals per day)."}), 400

    if amount == 10:
        conn.close()
        return jsonify({"message": "Impossible to withdraw 10 euros, the ATM does not offer 5 euro notes."}), 400
    if amount % 10 != 0 or amount < 10:
        conn.close()
        return jsonify({"message": "Invalid amount, it is impossible to withdraw a number that is not an integer or does not end in 0 or 5."}), 400

    if account_balance < amount:
        conn.close()
        return jsonify({"message": "You don't have enough money in your account"}), 400

    if amount > daily_withdrawal_limit:
        conn.close()
        return jsonify({"message": "Impossible, you have already withdrawn €200 today."}), 400

    new_balance = account_balance - amount
    new_daily_withdrawal_count = daily_withdrawal_count + 1
    remaining_limit = daily_withdrawal_limit - amount

    cursor.execute("UPDATE users SET balance = ?, daily_withdrawal_count = ?, daily_withdrawal_limit = ? WHERE username = ?", (new_balance, new_daily_withdrawal_count, remaining_limit, username))
    conn.commit()

    currentDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO transactions (user_id, date, amount) VALUES ((SELECT id FROM users WHERE username = ?), ?, ?)",
        (username, currentDate, amount))
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Withdrawal successful",
        "new_balance": new_balance,
        "remaining_limit": remaining_limit
    }), 200

@app.route('/withdraw-info', methods=['GET'])
def get_withdraw_info():
    username = request.args.get('username')

    if username is None:
        return jsonify({"message": "Username is missing"}), 400

    conn = sqlite3.connect("xefibank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance, daily_withdrawal_limit, daily_withdrawal_count FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data is None:
        return jsonify({"message": "User not found"}), 404

    account_balance = user_data[0]
    daily_withdrawal_limit = user_data[1]
    daily_withdrawal_count = user_data[2]

    response = {
        "username": username,
        "account_balance": account_balance,
        "daily_withdrawal_limit": daily_withdrawal_limit,
        "daily_withdrawal_count": daily_withdrawal_count
    }
    return jsonify(response)

@app.route('/user-withdrawals', methods=['GET'])
def get_user_withdrawals():
    username = request.args.get('username')

    if username is None:
        return jsonify({"message": "Username is missing"}), 400

    conn = sqlite3.connect("xefibank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, amount FROM transactions WHERE user_id = (SELECT id FROM users WHERE username = ?)", (username,))
    user_withdrawals = cursor.fetchall()
    conn.close()

    if not user_withdrawals:
        return jsonify({"message": "No withdrawals found for the user"}), 404

    withdrawals_list = []
    for withdrawal in user_withdrawals:
        withdrawals_list.append({
            "date": withdrawal[0],
            "amount": withdrawal[1]
        })

    response = {
        "username": username,
        "withdrawals": withdrawals_list
    }

    return jsonify(response)

@app.route('/user-balance', methods=['GET'])
def get_user_balance():
    username = request.args.get('username')

    if username is None:
        return jsonify({"message": "Username is missing"}), 400

    conn = sqlite3.connect("xefibank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
    user_balance = cursor.fetchone()
    conn.close()

    if user_balance is None:
        return jsonify({"message": "User not found"}), 404

    response = {
        "username": username,
        "balance": user_balance[0]
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
