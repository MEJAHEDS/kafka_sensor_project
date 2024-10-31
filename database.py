import sqlite3

# Créer une connexion à la base de données SQLite (ou la créer si elle n'existe pas)
conn = sqlite3.connect('sensor_data.db')

# Créer un curseur pour exécuter des commandes SQL
cursor = conn.cursor()

# Créer une table pour stocker les données des capteurs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id INTEGER,
        temperature REAL,
        humidity REAL,
        timestamp REAL
    )
''')

# Sauvegarder (commit) les changements et fermer la connexion
conn.commit()
conn.close()
