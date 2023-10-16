import hashlib
import Flask

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

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
                "message": "Authentication successful",
                "username": username,
                "account_balance": account_balance,
                "daily_withdrawal_limit": daily_withdrawal_limit
            }
        else:
            response = {
                "message": "Authentication failed"
            }
    else:
        response = {
            "message": "User not found"
        }

    conn.close()
    return jsonify(response)

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
        return jsonify({"message": "Daily withdrawal limit reached"})

    if amount % 10 != 0 or amount < 10:
        conn.close()
        return jsonify({"message": "Invalid withdrawal amount"})

    if account_balance < amount:
        conn.close()
        return jsonify({"message": "Insufficient balance"})

    if amount > daily_withdrawal_limit:
        conn.close()
        return jsonify({"message": "Amount exceeds daily withdrawal limit"})

    new_balance = account_balance - amount
    new_daily_withdrawal_count = daily_withdrawal_count + 1
    remaining_limit = daily_withdrawal_limit - amount

    cursor.execute("UPDATE users SET balance = ?, daily_withdrawal_count = ?, daily_withdrawal_limit = ? WHERE username = ?", (new_balance, new_daily_withdrawal_count, remaining_limit, username))
    conn.commit()

    cursor.execute("INSERT INTO transactions (user_id, date, amount) VALUES ((SELECT id FROM users WHERE username = ?), CURRENT_TIMESTAMP, ?)", (username, amount))
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Withdrawal successful",
        "new_balance": new_balance,
        "remaining_limit": remaining_limit
    })

if __name__ == '__main__':
    app.run(debug=True)
