import sqlite3

conn = sqlite3.connect("xefibank.db")
cursor = conn.cursor()

#Table Utilisateur
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    pincode TEXT,
    initial_balance REAL,
    daily_withdrawal_limit REAL, 
    daily_withdrawal_count INTEGER,
    balance REAL
)
''')

#Table Transaction
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    date TIMESTAMP,
    amount REAL
)
''')

conn.commit()

conn.close()

print("La base de données a été créée.")

